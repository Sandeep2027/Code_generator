import ast
from transformers import GPT2Tokenizer, GPT2LMHeadModel, pipeline
import torch
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Explicitly load GPT-2 with PyTorch
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2')
generator = pipeline('text-generation', model=model, tokenizer=tokenizer, framework='pt')

def generate_code(description, language):
    try:
        prompt = f"Generate optimized {language} code for: {description}"
        generated = generator(prompt, max_length=300, num_return_sequences=1, pad_token_id=tokenizer.eos_token_id)[0]['generated_text']
        
        code_start = generated.find('```')
        code_end = generated.rfind('```')
        code = generated[code_start+3:code_end].strip() if code_start != -1 and code_end != -1 else generated
        
        if language.lower() == 'python':
            try:
                ast.parse(code)
            except SyntaxError:
                code = _fix_python_syntax(code)
        elif language.lower() == 'javascript':
            code = _fix_javascript_syntax(code)
                
        logger.info(f"Generated code for: {description}")
        return code
    except Exception as e:
        logger.error(f"Code generation failed: {str(e)}")
        return f"// Error generating code: {str(e)}"

def _fix_python_syntax(code):
    lines = code.split('\n')
    fixed_lines = []
    indent_level = 0
    
    for line in lines:
        stripped = line.strip()
        if stripped:
            if stripped.endswith(':'):
                fixed_lines.append('    ' * indent_level + stripped)
                indent_level += 1
            else:
                fixed_lines.append('    ' * indent_level + stripped)
        if stripped.startswith('}') or stripped in ['else:', 'elif:', 'except:', 'finally:']:
            indent_level = max(0, indent_level - 1)
    
    return '\n'.join(fixed_lines)

def _fix_javascript_syntax(code):
    lines = code.split('\n')
    fixed_lines = []
    indent_level = 0
    
    for line in lines:
        stripped = line.strip()
        if stripped:
            if stripped.endswith('{'):
                fixed_lines.append('  ' * indent_level + stripped)
                indent_level += 1
            elif stripped.startswith('}'):
                indent_level = max(0, indent_level - 1)
                fixed_lines.append('  ' * indent_level + stripped)
            else:
                fixed_lines.append('  ' * indent_level + stripped)
    
    return '\n'.join(fixed_lines)
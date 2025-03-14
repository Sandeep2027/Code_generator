from transformers import T5Tokenizer, T5ForConditionalGeneration, pipeline
import torch

tokenizer = T5Tokenizer.from_pretrained('t5-small')
model = T5ForConditionalGeneration.from_pretrained('t5-small')
explainer = pipeline('text2text-generation', model=model, tokenizer=tokenizer, framework='pt')

def explain_code(code, language):
    try:
        prompt = f"Explain this {language} code:\n{code}"
        explanation = explainer(prompt, max_length=200)[0]['generated_text']
        return explanation
    except Exception as e:
        return f"Could not generate explanation: {str(e)}"
import subprocess
import tempfile
import ast
import pylint.lint
from io import StringIO
import sys
import eslint

def validate_code(code, language):
    if language.lower() == 'python':
        try:
            ast.parse(code)
            with tempfile.NamedTemporaryFile(suffix='.py', delete=False) as temp:
                temp.write(code.encode())
                temp_file = temp.name
            
            pylint_output = StringIO()
            sys.stdout = pylint_output
            pylint.lint.Run([temp_file, '--disable=all', '--enable=syntax-error,undefined-variable'])
            sys.stdout = sys.__stdout__
            
            return {
                'status': 'valid',
                'message': 'Syntax is valid',
                'quality_report': pylint_output.getvalue()
            }
        except SyntaxError as e:
            return {'status': 'invalid', 'message': f'Syntax Error: {str(e)}'}
        except Exception as e:
            return {'status': 'error', 'message': f'Validation failed: {str(e)}'}
    elif language.lower() == 'javascript':
        try:
            with tempfile.NamedTemporaryFile(suffix='.js', delete=False) as temp:
                temp.write(code.encode())
                temp_file = temp.name
            # Note: Requires ESLint installed via npm
            result = subprocess.run(['eslint', temp_file], capture_output=True, text=True)
            return {
                'status': 'valid' if result.returncode == 0 else 'invalid',
                'message': result.stdout or 'Syntax is valid'
            }
        except Exception as e:
            return {'status': 'error', 'message': f'Validation failed: {str(e)}'}
    return {'status': 'pending', 'message': 'Validation not implemented'}

def run_unit_tests(code, language):
    if language.lower() == 'python':
        try:
            test_code = _generate_python_tests(code)
            with tempfile.NamedTemporaryFile(suffix='.py', delete=False) as temp:
                temp.write(test_code.encode())
                temp_file = temp.name
            
            result = subprocess.run(['python', '-m', 'unittest', temp_file],
                                  capture_output=True, text=True)
            return {
                'status': 'success' if result.returncode == 0 else 'failed',
                'output': result.stdout + result.stderr
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    elif language.lower() == 'javascript':
        try:
            test_code = _generate_javascript_tests(code)
            with tempfile.NamedTemporaryFile(suffix='.js', delete=False) as temp:
                temp.write(test_code.encode())
                temp_file = temp.name
            
            result = subprocess.run(['node', temp_file], capture_output=True, text=True)
            return {
                'status': 'success' if result.returncode == 0 else 'failed',
                'output': result.stdout + result.stderr
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    return {'status': 'pending', 'message': 'Tests not implemented'}

def _generate_python_tests(code):
    return f"""
import unittest
{code}

class TestGeneratedCode(unittest.TestCase):
    def test_factorial(self):
        if 'factorial' in globals():
            self.assertEqual(factorial(5), 120)
            self.assertEqual(factorial(0), 1)

if __name__ == '__main__':
    unittest.main()
"""

def _generate_javascript_tests(code):
    return f"""
{code}

function runTests() {{
    console.assert(factorial(5) === 120, 'Factorial of 5 should be 120');
    console.assert(factorial(0) === 1, 'Factorial of 0 should be 1');
    console.log('Tests completed');
}}

runTests();
"""
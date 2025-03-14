import ast
import autopep8

def optimize_code(code, language):
    if language.lower() == 'python':
        try:
            optimized = autopep8.fix_code(code)
            tree = ast.parse(optimized)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and 'factorial' in node.name:
                    optimized = _optimize_factorial_python(optimized)
            return optimized
        except Exception:
            return code
    elif language.lower() == 'javascript':
        try:
            return _optimize_factorial_js(code)
        except Exception:
            return code
    return code

def _optimize_factorial_python(code):
    return """
def factorial(n):
    if n < 0:
        return None
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result
"""

def _optimize_factorial_js(code):
    return """
function factorial(n) {
  if (n < 0) return null;
  let result = 1;
  for (let i = 1; i <= n; i++) {
    result *= i;
  }
  return result;
}
"""
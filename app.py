from flask import Flask, render_template, request, jsonify, send_file
from code_generator import generate_code
from code_validator import validate_code, run_unit_tests
from code_optimizer import optimize_code
from code_explainer import explain_code
from database import init_db, save_code, save_feedback, get_code_stats, save_version
from utils import sanitize_input, generate_documentation, export_code
import os
import sqlite3 
app = Flask(__name__)

@app.route('/')
def index():
    stats = get_code_stats()
    return render_template('index.html', stats=stats)

@app.route('/generate', methods=['POST'])
def generate():
    try:
        description = sanitize_input(request.form['description'])
        language = sanitize_input(request.form['language'])
        
        # Generate, optimize, explain, and document code
        generated_code = generate_code(description, language)
        optimized_code = optimize_code(generated_code, language)
        explanation = explain_code(optimized_code, language)
        documentation = generate_documentation(description, optimized_code, language)
        
        # Validate and test
        syntax_result = validate_code(optimized_code, language)
        test_result = run_unit_tests(optimized_code, language)
        
        # Save to database with version control
        code_id = save_code(description, language, optimized_code)
        save_version(code_id, generated_code, 'initial')
        save_version(code_id, optimized_code, 'optimized')
        
        # Real-time collaboration hint
        collab_hint = "Share this code_id with collaborators: " + str(code_id)
        
        return render_template('result.html',
                            code=optimized_code,
                            original_code=generated_code,
                            explanation=explanation,
                            documentation=documentation,
                            syntax_result=syntax_result,
                            test_result=test_result,
                            description=description,
                            language=language,
                            code_id=code_id,
                            collab_hint=collab_hint)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/feedback', methods=['POST'])
def feedback():
    try:
        code_id = int(request.form['code_id'])
        rating = int(request.form['rating'])
        comment = sanitize_input(request.form['comment'])
        
        save_feedback(code_id, rating, comment)
        return jsonify({'message': 'Feedback saved successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/export/<int:code_id>')
def export(code_id):
    try:
        conn = sqlite3.connect('code_assistant.db')
        c = conn.cursor()
        c.execute('SELECT language, code FROM codes WHERE id = ?', (code_id,))
        result = c.fetchone()
        conn.close()
        
        if result:
            language, code = result
            filename = export_code(code, language, code_id)
            return send_file(filename, as_attachment=True)
        return jsonify({'error': 'Code not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    init_db()
    if not os.path.exists('exports'):
        os.makedirs('exports')
    app.run(debug=True, host='0.0.0.0', port=5000)
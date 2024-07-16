from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
import spacy
from openai import OpenAI
import os
import PyPDF2
from prompts import prompts

app = Flask(__name__, template_folder='public', static_folder='public')
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload_cv', methods=['POST'])
def upload_cv():
    try:
        file = request.files['cv']
        if not file:
            return jsonify({"error": "No file provided"}), 400
        
        filename = secure_filename(file.filename)
        upload_folder = os.path.abspath(app.config['UPLOAD_FOLDER'])
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, filename)
        
        file.save(file_path)
        
        if not os.path.exists(file_path):
            return jsonify({"error": "File upload failed"}), 500
        
        cv_text = read_pdf(file_path)
        if cv_text is None:
            return jsonify({"error": "Failed to read PDF content"}), 500
        
        return jsonify({
            "message": "CV uploaded and processed",
            "filename": filename,
            "content": cv_text
        })
    
    except Exception as e:
        print(f"Error during file upload or processing: {str(e)}")
        return jsonify({"error": str(e)}), 500

def read_pdf(file_path):
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
        return text if text else None
    except Exception as e:
        print(f"Error reading PDF: {str(e)}")
        return None


@app.route('/upload_notes', methods=['POST'])
def upload_notes():
    notes = request.form['notes']
    return jsonify({"message": "Notes received", "notes": notes})

@app.route('/process_cv', methods=['POST'])
def process_cv():
    try:
        filename = request.form['filename']
        notes = request.form['notes']

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if not os.path.exists(file_path):
            return jsonify({"error": "File not found"}), 404

        cv_text = read_pdf(file_path)
        if cv_text is None:
            return jsonify({"error": "Failed to read PDF content"}), 500

        # Generate new CV with GPT
        client = OpenAI()
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o",  # Use an available engine
                temperature=0.1,
                messages=[
                    {"role": "system", "content": prompts},
                    {"role": "user", "content": f"Original CV: {cv_text}\n\nNotes: {notes}\n\nGenerate a new, improved CV."}
                ]
            )
        except client.error.InvalidRequestError as e:
            if 'model_not_found' in str(e):
                print("Error: The specified model `gpt-4o` does not exist or you do not have access to it.")
                print("Please check if you have credits on your OpenAI account at https://platform.openai.com/settings/organization/billing/overview")
            else:
                raise

        new_cv = response.choices[0].message.content
        return jsonify({"new_cv": new_cv})

    except Exception as e:
        print(f"Error processing CV: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

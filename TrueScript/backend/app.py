# backend/app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import pymongo
from plagiarism_detector import check_plagiarism

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# MongoDB setup
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client['truescript']
results_collection = db['results']

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Run plagiarism detection
    result = check_plagiarism(filepath)

    # Store result in MongoDB
    results_collection.insert_one({
        'filename': filename,
        'plagiarism_score': result['score'],
        'similarity_details': result['details']
    })

    return jsonify(result)

@app.route('/results', methods=['GET'])
def get_results():
    data = list(results_collection.find({}, {'_id': 0}))  # Exclude _id
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)

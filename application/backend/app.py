from flask import Flask, jsonify, request
from database import get_sections, generate_story_options  # Import functions from database.py

app = Flask(__name__)

@app.route('/sections', methods=['GET'])
def sections():
    sections = get_sections()
    return jsonify(sections)

@app.route('/generate_story', methods=['POST'])
def generate_story():
    data = request.get_json()
    section_text = data.get('section_text', '')
    story, paths = generate_story_options(section_text)
    return jsonify({"story": story, "paths": paths})

if __name__ == '__main__':
    app.run(debug=True)
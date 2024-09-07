from flask import Flask, jsonify, request
from database import get_sections, get_section_by_id
import google.generativeai as genai
import re

app = Flask(__name__)

# Initialize the Gemini API
api_key = "AIzaSyCJRS1Wdp-ggwC4X7hzrAgMx3nzr"
genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# Endpoint to get all sections
@app.route('/api/sections', methods=['GET'])
def get_all_sections():
    sections = get_sections()
    return jsonify(sections)

# Endpoint to generate story options based on the section text
@app.route('/api/generate_story', methods=['POST'])
def generate_story():
    data = request.get_json()
    section_id = data.get('section_id')
    section_text = get_section_by_id(section_id)
    
    story, story_options = generate_story_options(section_text)
    
    return jsonify({
        "story": story,
        "options": story_options
    })

# Function to generate story options using Gemini API
def generate_story_options(section_text):
    prompt = (
        "You are a writer for a 'Choose Your Own Adventure' story to teach Carpentry and Woodwork. "
        "Based on the following section of text: \n\n'{text}'\n\n"
        "First, create a full story based on the text. Then, provide three distinct story paths labeled as Path 1, Path 2, and Path 3, "
        "that the reader can choose from, each path following the main story."
    )
    
    response = model.generate_content(prompt.format(text=section_text))
    
    # Parse the response to separate the main story and paths
    if response and response.text:
        # Split the response into story and paths
        parts = re.split(r'\n?Path \d+', response.text)
        story = parts[0].strip()
        paths = [part.strip() for part in parts[1:] if part.strip()]
        
        # Ensure we have exactly three paths
        while len(paths) < 3:
            paths.append(f"Path {len(paths) + 1}: No content generated")
        
        return story, [f"Path {i + 1}: {path}" for i, path in enumerate(paths[:3])]

    return "No story generated.", ["Path 1: No content generated", "Path 2: No content generated", "Path 3: No content generated"]

if __name__ == "__main__":
    app.run(debug=True)

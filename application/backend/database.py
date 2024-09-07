import sqlite3
import re
from genai import configure, GenerativeModel

# Configure the Gemini API
api_key = "AIzaSyCJRS1Wdp-ggwC4X7hzrAgMx3nzD0ioPp4"
configure(api_key=api_key)
model = GenerativeModel(model_name="gemini-1.5-flash")

def get_sections():
    conn = sqlite3.connect('sections.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM sections')
    sections = cursor.fetchall()
    conn.close()
    return [{"id": row[0], "content": row[1]} for row in sections]

def generate_story_options(section_text):
    prompt = (
        "You are a writer for a 'Choose Your Own Adventure' story to teach Carpentry and Woodwork. "
        "Based on the following section of text: \n\n'{text}'\n\n"
        "First, create a full story based on the text. Then, provide three distinct story paths labeled as Path 1, Path 2, and Path 3, "
        "that the reader can choose from, each path following the main story."
    )
    
    response = model.generate_content(prompt.format(text=section_text))
    
    if response and response.text:
        parts = re.split(r'\n?Path \d+', response.text)
        story = parts[0].strip()
        paths = [part.strip() for part in parts[1:] if part.strip()]
        
        while len(paths) < 3:
            paths.append(f"Path {len(paths) + 1}: No content generated")
        
        return story, [f"Path {i + 1}: {path}" for i, path in enumerate(paths[:3])]

    return "No story generated.", ["Path 1: No content generated", "Path 2: No content generated", "Path 3: No content generated"]
import streamlit as st
from pdf2image import convert_from_path
import pytesseract
import re
import google.generativeai as genai

# Configure the Gemini API
api_key = "AIzaSyCJRS1Wdp-ggwC4X7hzrAgMx3nzD0ioPp4"
genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# Function to perform OCR on selected PDF pages
def extract_text_with_ocr(pdf_path, start_page, end_page):
    pages = convert_from_path(pdf_path, first_page=start_page + 1, last_page=end_page)
    chapter_text = ""
    
    for page in pages:
        text = pytesseract.image_to_string(page)
        chapter_text += text
    
    return chapter_text

# Function to split text on headers
def split_text_on_headers(text):
    # Regex to match headers like '1.0 Hammer', '2.0 Saws'
    header_pattern = re.compile(r'\n?\d+\.0([^\n]+)*')
    
    # Find all headers and their positions
    headers = list(header_pattern.finditer(text))
    
    sections = []
    start = 0
    
    # Extract text between headers
    for header in headers:
        header_start = header.start()
        header_end = header.end()
        next_header_start = headers[headers.index(header) + 1].start() if (headers.index(header) + 1) < len(headers) else None
        
        # Extract section text
        section_text = text[start:header_start].strip()
        if section_text:
            sections.append(section_text)
        
        # Update start to next header
        start = header_start
        
    # Add last section after the last header
    final_section = text[start:].strip()
    if final_section:
        sections.append(final_section)
    
    return sections

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

# Streamlit app
def main():
    # Display "Choose Your Own Adventure" on the home page
    st.title("Choose Your Own Adventure Story")

    # Background processing
    with st.spinner("Processing OCR and generating story paths..."):
        # Define PDF path and page range
        pdf_path = 'resource/Carpentry and Woodwork-output.pdf'
        start_page = 8
        end_page = 20
        
        # Extract text using OCR
        chapter_text = extract_text_with_ocr(pdf_path, start_page, end_page)
        
        # Split the text into sections based on headers
        sections = split_text_on_headers(chapter_text)
    
    # Let the user select a section from the dropdown
    section_options = [f"Section {i + 1}" for i in range(len(sections))]
    selected_section_index = st.selectbox("Choose a section to start your adventure:", list(range(len(sections))), format_func=lambda x: section_options[x])
    
    # Display the text of the selected section
    selected_section = sections[selected_section_index]
    st.subheader(f"Section {selected_section_index + 1}: Story Options")
    st.text_area(f"Text from Section {selected_section_index + 1}", selected_section, height=200)
    
    # Generate and display the story options for the selected section
    story, story_options = generate_story_options(selected_section)
    
    # Display the generated story
    st.write("Main Story:")
    st.write(story)
    
    # Display the generated story options
    for option in story_options:
        st.write(option)
    
    # Let the user choose one of the options
    choice = st.radio(f"Choose your path for Section {selected_section_index + 1}:", [f"Path {j + 1}" for j in range(len(story_options))])
    st.write(f"You selected: {choice}")

if __name__ == '__main__':
    main()

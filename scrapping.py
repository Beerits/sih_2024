import sqlite3
import re
from pdf2image import convert_from_path
import pytesseract

# Function to extract text from PDF using OCR
def extract_text_with_ocr(pdf_path, start_page, end_page):
    pages = convert_from_path(pdf_path, first_page=start_page + 1, last_page=end_page)
    chapter_text = ""
    
    for page in pages:
        text = pytesseract.image_to_string(page)
        chapter_text += text
    
    return chapter_text

# Function to split text based on headers
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

# Function to save sections to SQLite database
def save_sections_to_db(sections):
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('sections.db')
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sections (
            section_number INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL
        )
    ''')
    
    # Insert sections into the table
    for idx, section in enumerate(sections):
        cursor.execute('INSERT INTO sections (content) VALUES (?)', (section,))
    
    # Commit the transaction and close the connection
    conn.commit()
    conn.close()

# Main flow to extract, split, and store sections
pdf_path = 'resource/Carpentry and Woodwork-output.pdf'
start_page = 8
end_page = 20

# Extract text using OCR
chapter_text = extract_text_with_ocr(pdf_path, start_page, end_page)

# Split the text into sections based on headers
sections = split_text_on_headers(chapter_text)

# Save the sections to the database
save_sections_to_db(sections)

print("Sections successfully saved to the database!")

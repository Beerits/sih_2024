import sqlite3

# Function to get all sections from the database
def get_sections():
    conn = sqlite3.connect('sections.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT section_number, content FROM sections")
    sections = cursor.fetchall()
    
    conn.close()
    
    return [{"section_number": row[0], "content": row[1]} for row in sections]

# Function to get a specific section by its ID
def get_section_by_id(section_number):
    conn = sqlite3.connect('sections.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT content FROM sections WHERE section_number=?", (section_number,))
    section = cursor.fetchone()
    
    conn.close()
    
    return section[0] if section else None

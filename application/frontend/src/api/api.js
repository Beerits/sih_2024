const API_URL = 'http://localhost:5000';

export const fetchSections = async () => {
    const response = await fetch(`${API_URL}/sections`);
    return response.json();
};

export const generateStory = async (sectionText) => {
    const response = await fetch(`${API_URL}/generate_story`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ section_text: sectionText }),
    });
    return response.json();
};
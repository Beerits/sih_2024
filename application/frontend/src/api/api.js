export async function fetchSections() {
    const response = await fetch('/api/sections');
    return response.json();
}

export async function generateStory(section_id) {
    const response = await fetch('/api/generate_story', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ section_id }),
    });

    return response.json();
}

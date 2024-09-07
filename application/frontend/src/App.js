import React, { useState, useEffect } from 'react';
import SectionSelector from './components/SectionSelector';
import { fetchSections, generateStory } from './api/api';

function App() {
    const [sections, setSections] = useState([]);
    const [selectedSection, setSelectedSection] = useState(null);
    const [story, setStory] = useState('');
    const [storyOptions, setStoryOptions] = useState([]);

    useEffect(() => {
        async function getSections() {
            const sections = await fetchSections();
            setSections(sections);
        }

        getSections();
    }, []);

    const handleSectionSelect = async (section) => {
        setSelectedSection(section);
        const { story, options } = await generateStory(section.section_number);
        setStory(story);
        setStoryOptions(options);
    };

    return (
        <div>
            <h1>Carpentry Adventure App</h1>
            <SectionSelector sections={sections} onSelect={handleSectionSelect} />
            {selectedSection && (
                <div>
                    <h2>Section {selectedSection.section_number}: Story Options</h2>
                    <p>{story}</p>
                    <ul>
                        {storyOptions.map((option, index) => (
                            <li key={index}>{option}</li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
}

export default App;

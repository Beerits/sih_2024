import React, { useEffect, useState } from 'react';
import { fetchSections, generateStory } from '../api/api';

const SectionSelector = () => {
    const [sections, setSections] = useState([]);
    const [selectedSection, setSelectedSection] = useState(null);
    const [story, setStory] = useState('');
    const [storyOptions, setStoryOptions] = useState([]);

    useEffect(() => {
        const loadSections = async () => {
            const response = await fetchSections();
            setSections(response);
        };
        loadSections();
    }, []);

    const handleSectionChange = async (event) => {
        const index = event.target.value;
        setSelectedSection(sections[index]);

        const response = await generateStory(sections[index].content);
        setStory(response.story);
        setStoryOptions(response.paths);
    };

    return (
        <div>
            <select onChange={handleSectionChange}>
                {sections.map((section, index) => (
                    <option key={section.id} value={index}>
                        Section {section.id}
                    </option>
                ))}
            </select>

            {selectedSection && (
                <div>
                    <h2>Section {selectedSection.id}</h2>
                    <p>{selectedSection.content}</p>
                    <h3>Main Story:</h3>
                    <p>{story}</p>
                    <h3>Story Options:</h3>
                    {storyOptions.map((option, index) => (
                        <p key={index}>{option}</p>
                    ))}
                </div>
            )}
        </div>
    );
};

export default SectionSelector;
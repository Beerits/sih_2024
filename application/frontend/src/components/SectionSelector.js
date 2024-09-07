import React from 'react';

function SectionSelector({ sections, onSelect }) {
    return (
        <div>
            <select onChange={(e) => onSelect(sections[e.target.value])}>
                <option value="">Select a section...</option>
                {sections.map((section, index) => (
                    <option key={index} value={index}>
                        Section {section.section_number}
                    </option>
                ))}
            </select>
        </div>
    );
}

export default SectionSelector;

// Entry point for Vite
// We keep data JSON under public/data; renderer remains plain JS

import './styles/utilities.css';
import '../public/styles.css';
import '../public/map-renderer.js';

// Legend toggle functionality
document.addEventListener('DOMContentLoaded', () => {
    const mainToggleButton = document.getElementById('legendToggle');
    const legendContent = document.getElementById('legendContent');
    const secondaryToggleButton = document.getElementById('legendToggleSecondary');
    const expandableSection = document.getElementById('legendExpandable');
    
    // Main toggle (shows/hides entire legend content)
    if (mainToggleButton && legendContent) {
        mainToggleButton.addEventListener('click', () => {
            const isExpanded = legendContent.style.display !== 'none';
            
            if (isExpanded) {
                // Collapse entire legend
                legendContent.style.display = 'none';
                mainToggleButton.innerHTML = '<i class="fa fa-chevron-down"></i> Show Legend';
            } else {
                // Expand legend
                legendContent.style.display = 'block';
                mainToggleButton.innerHTML = '<i class="fa fa-chevron-up"></i> Hide Legend';
            }
        });
    }
    
    // Secondary toggle (shows/hides POI and train details)
    if (secondaryToggleButton && expandableSection) {
        secondaryToggleButton.addEventListener('click', () => {
            const isExpanded = expandableSection.style.display !== 'none';
            
            if (isExpanded) {
                // Collapse POI/train details
                expandableSection.style.display = 'none';
                secondaryToggleButton.innerHTML = '<i class="fa fa-chevron-down"></i> Show More';
            } else {
                // Expand POI/train details
                expandableSection.style.display = 'block';
                secondaryToggleButton.innerHTML = '<i class="fa fa-chevron-up"></i> Show Less';
            }
        });
    }
});




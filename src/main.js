// Entry point for Vite
// We keep data JSON under public/data; renderer remains plain JS

import '../public/styles.css';
import '../public/map-renderer.js';

// Legend toggle functionality
document.addEventListener('DOMContentLoaded', () => {
    const toggleButton = document.getElementById('legendToggle');
    const expandableSection = document.getElementById('legendExpandable');
    
    if (toggleButton && expandableSection) {
        toggleButton.addEventListener('click', () => {
            const isExpanded = expandableSection.style.display !== 'none';
            
            if (isExpanded) {
                // Collapse
                expandableSection.style.display = 'none';
                toggleButton.innerHTML = '<i class="fa fa-chevron-down"></i> Show More';
            } else {
                // Expand
                expandableSection.style.display = 'block';
                toggleButton.innerHTML = '<i class="fa fa-chevron-up"></i> Show Less';
            }
        });
    }
});




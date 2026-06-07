// Theme Switcher Functionality
const themes = {
    pink: {
        primary: '#e91e63',
        primaryDark: '#c2185b',
        primaryLight: '#f8bbd0'
    },
    purple: {
        primary: '#9c27b0',
        primaryDark: '#7b1fa2',
        primaryLight: '#e1bee7'
    },
    blue: {
        primary: '#2196f3',
        primaryDark: '#1976d2',
        primaryLight: '#bbdefb'
    },
    green: {
        primary: '#4caf50',
        primaryDark: '#388e3c',
        primaryLight: '#c8e6c9'
    },
    orange: {
        primary: '#ff9800',
        primaryDark: '#f57c00',
        primaryLight: '#ffe0b2'
    },
    red: {
        primary: '#f44336',
        primaryDark: '#d32f2f',
        primaryLight: '#ffcdd2'
    },
    teal: {
        primary: '#009688',
        primaryDark: '#00796b',
        primaryLight: '#b2dfdb'
    }
};

function setTheme(themeName) {
    const theme = themes[themeName];
    if (!theme) return;
    
    document.documentElement.style.setProperty('--primary-color', theme.primary);
    document.documentElement.style.setProperty('--primary-dark', theme.primaryDark);
    document.documentElement.style.setProperty('--primary-light', theme.primaryLight);
    
    // Save theme preference
    localStorage.setItem('hafsacart-theme', themeName);
}

function loadSavedTheme() {
    const savedTheme = localStorage.getItem('hafsacart-theme');
    if (savedTheme && themes[savedTheme]) {
        setTheme(savedTheme);
    }
}

// Add theme selector to page (optional)
function addThemeSelector() {
    const selectorHtml = `
        <div class="theme-selector" style="position: fixed; bottom: 100px; right: 20px; z-index: 999;">
            <div class="dropdown">
                <button class="btn btn-primary rounded-circle" style="width: 50px; height: 50px;" data-bs-toggle="dropdown">
                    🎨
                </button>
                <ul class="dropdown-menu">
                    <li><a class="dropdown-item" href="#" onclick="setTheme('pink')">🌸 Pink Theme</a></li>
                    <li><a class="dropdown-item" href="#" onclick="setTheme('purple')">🟣 Purple Theme</a></li>
                    <li><a class="dropdown-item" href="#" onclick="setTheme('blue')">🔵 Blue Theme</a></li>
                    <li><a class="dropdown-item" href="#" onclick="setTheme('green')">🟢 Green Theme</a></li>
                    <li><a class="dropdown-item" href="#" onclick="setTheme('orange')">🟠 Orange Theme</a></li>
                    <li><a class="dropdown-item" href="#" onclick="setTheme('red')">🔴 Red Theme</a></li>
                    <li><a class="dropdown-item" href="#" onclick="setTheme('teal')">💚 Teal Theme</a></li>
                </ul>
            </div>
        </div>
    `;
    document.body.insertAdjacentHTML('beforeend', selectorHtml);
}

// Load saved theme on page load
document.addEventListener('DOMContentLoaded', () => {
    loadSavedTheme();
    // addThemeSelector(); // Uncomment to add theme picker
});
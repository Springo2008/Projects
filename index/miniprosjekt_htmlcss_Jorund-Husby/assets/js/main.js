// JavaScript for Husby Drone Website
class DroneWebsite {
    constructor() {
        this.initBurgerMenu();
        this.initEventListeners();
    }
    
    // Burgermeny funksjonalitet
    initBurgerMenu() {
        const burger = document.querySelector('.burger');
        const dropdown = document.getElementById('dropdownMenu');
        
        if (burger && dropdown) {
            // Fjern eventuell eksisterende onclick
            burger.removeAttribute('onclick');
            
            burger.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                dropdown.classList.toggle('show');
            });
        }
    }
    
    // Andre event listeners
    initEventListeners() {
        // Lukk menyen hvis man klikker utenfor
        document.addEventListener('click', (event) => {
            const dropdown = document.getElementById('dropdownMenu');
            const burger = document.querySelector('.burger');
            
            // Sjekk om klikket var på burgermeny eller dropdown
            if (!burger?.contains(event.target) && !dropdown?.contains(event.target)) {
                if (dropdown && dropdown.classList.contains('show')) {
                    dropdown.classList.remove('show');
                }
            }
        });
        
        // Smooth scrolling for interne lenker
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth'
                    });
                }
            });
        });
    }
}

//
function toggleMenu() {
    const dropdown = document.getElementById('dropdownMenu');
    if (dropdown) {
        dropdown.classList.toggle('show');
    }
}

// Initialiser når DOM er lastet
document.addEventListener('DOMContentLoaded', () => {
    new DroneWebsite();
});
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
                const isOpen = dropdown.classList.toggle('show');
                burger.setAttribute('aria-expanded', String(isOpen));
                if (isOpen) {
                    dropdown.querySelector('a')?.focus();
                }
            });

            dropdown.addEventListener('click', (event) => {
                if (event.target instanceof HTMLElement && event.target.tagName === 'A') {
                    this.closeMenu(dropdown, burger);
                }
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
                dropdown && burger && this.closeMenu(dropdown, burger);
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

        document.addEventListener('keydown', (event) => {
            if (event.key === 'Escape') {
                const dropdown = document.getElementById('dropdownMenu');
                const burger = document.querySelector('.burger');
                if (dropdown && burger && dropdown.classList.contains('show')) {
                    this.closeMenu(dropdown, burger);
                    burger.focus();
                }
            }
        });
    }

    closeMenu(dropdown, burger) {
        dropdown.classList.remove('show');
        burger.setAttribute('aria-expanded', 'false');
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
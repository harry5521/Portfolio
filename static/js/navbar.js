console.log('🔍 navbar.js STARTED');

document.addEventListener('DOMContentLoaded', function () {
    const navToggle = document.getElementById('nav-toggle');
    const mobileMenu = document.getElementById('mobile-menu');
    const menuOverlay = document.getElementById('menu-overlay');

    console.log('🔍 Elements:', {
        navToggle: !!navToggle,
        mobileMenu: !!mobileMenu,
        menuOverlay: !!menuOverlay,
        mobileLinks: document.querySelectorAll('.mobile-nav-link').length
    });

    if (!navToggle || !mobileMenu) {
        console.error('❌ Navbar elements not found!');
        return;
    }

    let isOpen = false;

    function openMenu() {
        isOpen = true;

        mobileMenu.classList.remove(
            'max-h-0',
            'opacity-0',
            'pointer-events-none'
        );

        mobileMenu.classList.add(
            'max-h-[500px]',
            'opacity-100',
            'pointer-events-auto'
        );

        if (menuOverlay) {
            menuOverlay.classList.remove('hidden');
        }

        document.body.style.overflow = 'hidden';

        navToggle.setAttribute('aria-expanded', 'true');

        console.log('✅ Menu OPENED');
    }

    function closeMenu() {
        isOpen = false;

        mobileMenu.classList.add(
            'max-h-0',
            'opacity-0',
            'pointer-events-none'
        );

        mobileMenu.classList.remove(
            'max-h-[500px]',
            'opacity-100',
            'pointer-events-auto'
        );

        if (menuOverlay) {
            menuOverlay.classList.add('hidden');
        }

        document.body.style.overflow = '';

        navToggle.setAttribute('aria-expanded', 'false');

        console.log('✅ Menu CLOSED');
    }

    function toggleMenu() {
        if (isOpen) {
            closeMenu();
        } else {
            openMenu();
        }
    }

    // Hamburger button
    navToggle.addEventListener('click', function () {
        console.log('🔍 TOGGLE CLICKED');
        toggleMenu();
    });

    // Mobile navigation links
    document.querySelectorAll('.mobile-nav-link').forEach(function (link) {
        link.addEventListener('click', function () {
            console.log('🔗 Mobile link clicked:', this.textContent.trim());

            // IMPORTANT:
            // Don't prevent the default anchor behavior.
            // Browser will handle href="#section" normally.
            closeMenu();
        });
    });

    // Overlay
    if (menuOverlay) {
        menuOverlay.addEventListener('click', function () {
            console.log('🔍 OVERLAY CLICKED');
            closeMenu();
        });
    }

    // ESC key
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && isOpen) {
            closeMenu();
        }
    });

    // Close menu when switching to desktop
    window.addEventListener('resize', function () {
        if (window.innerWidth >= 768 && isOpen) {
            closeMenu();
        }
    });
});

console.log('🔍 navbar.js LOADED');

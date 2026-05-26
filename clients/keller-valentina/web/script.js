document.addEventListener('DOMContentLoaded', () => {
    // Navbar Scroll Morph Effect
    const navbar = document.getElementById('navbar');
    if (navbar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) { // Adjust scroll threshold as needed
                navbar.classList.add('navbar--scrolled');
            } else {
                navbar.classList.remove('navbar--scrolled');
            }
        });
    }

    // Mobile Menu Toggle
    const navbarToggle = document.querySelector('.navbar__toggle');
    const mobileMenu = document.querySelector('.navbar__mobile-menu');
    const navbarLinksMobile = document.querySelectorAll('.navbar__mobile-menu a');

    if (navbarToggle && mobileMenu) {
        navbarToggle.addEventListener('click', () => {
            navbarToggle.classList.toggle('is-active');
            mobileMenu.classList.toggle('is-active');
            document.body.classList.toggle('no-scroll'); // Prevent scrolling when menu is open
        });

        // Close mobile menu when a link is clicked
        navbarLinksMobile.forEach(link => {
            link.addEventListener('click', () => {
                navbarToggle.classList.remove('is-active');
                mobileMenu.classList.remove('is-active');
                document.body.classList.remove('no-scroll');
            });
        });
    }


    // Smooth Scrolling for Navbar Links
    document.querySelectorAll('.navbar__menu a[href^="#"], .navbar__mobile-menu a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            if (targetElement) {
                const offset = navbar.offsetHeight; // Get dynamic navbar height
                window.scrollTo({
                    top: targetElement.offsetTop - offset,
                    behavior: 'smooth'
                });

                // Update active link class for desktop menu (only when clicked)
                // This will be overridden by the Intersection Observer, but good for immediate feedback
                document.querySelectorAll('.navbar__menu .navbar__link').forEach(link => link.classList.remove('navbar__link--active'));
                this.classList.add('navbar__link--active');
            }
        });
    });

    // Intersection Observer for Scroll Reveal
    const revealElements = document.querySelectorAll('.reveal-on-scroll');

    const observerOptions = {
        root: null, // viewport
        rootMargin: '0px',
        threshold: 0.1 // Percentage of element visible to trigger
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
                observer.unobserve(entry.target); // Stop observing once visible
            }
        });
    }, observerOptions);

    revealElements.forEach(element => {
        observer.observe(element);
    });

    // Observer to update active navigation link on scroll
    // Targets main sections and specific service cards
    const sectionsAndCards = document.querySelectorAll('main section[id], .service-card[id]'); 
    const navLinksDesktop = document.querySelectorAll('.navbar__menu .navbar__link');
    const navLinksMobile = document.querySelectorAll('.navbar__mobile-menu .navbar__link');

    const sectionObserverOptions = {
        root: null,
        rootMargin: '-50% 0px -49% 0px', // When section midpoint is in view, adjusted to be more precise
        threshold: 0 // Only needs to enter/exit viewport
    };

    const sectionObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const id = entry.target.id;
                
                // Update desktop links
                navLinksDesktop.forEach(link => {
                    link.classList.remove('navbar__link--active');
                    if (link.getAttribute('href') === `#${id}`) {
                        link.classList.add('navbar__link--active');
                    }
                });

                // Update mobile links
                navLinksMobile.forEach(link => {
                    link.classList.remove('navbar__link--active');
                    if (link.getAttribute('href') === `#${id}`) {
                        link.classList.add('navbar__link--active');
                    }
                });
            }
        });
    }, sectionObserverOptions);

    sectionsAndCards.forEach(element => {
        sectionObserver.observe(element);
    });

    // Initial check for active link based on URL hash (if direct link with hash)
    const currentHash = window.location.hash;
    if (currentHash) {
        const activeLink = document.querySelector(`.navbar__menu .navbar__link[href="${currentHash}"]`);
        if (activeLink) {
            document.querySelectorAll('.navbar__menu .navbar__link').forEach(link => link.classList.remove('navbar__link--active'));
            activeLink.classList.add('navbar__link--active');
        }
    } else {
        // Default to Home if no hash and on desktop view initially
        const homeLink = document.querySelector('.navbar__menu .navbar__link[href="#home"]');
        if (homeLink && window.scrollY < 50) { 
            homeLink.classList.add('navbar__link--active');
        }
    }
});
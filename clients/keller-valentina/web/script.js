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

    // Smooth Scrolling for Navbar Links
    document.querySelectorAll('.navbar__menu a[href^="#"]').forEach(anchor => {
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

                // Update active link class
                document.querySelectorAll('.navbar__link').forEach(link => link.classList.remove('navbar__link--active'));
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

    // Initial check for active link based on URL hash
    const currentHash = window.location.hash;
    if (currentHash) {
        const activeLink = document.querySelector(`.navbar__link[href="${currentHash}"]`);
        if (activeLink) {
            document.querySelectorAll('.navbar__link').forEach(link => link.classList.remove('navbar__link--active'));
            activeLink.classList.add('navbar__link--active');
        }
    } else {
        // Default to Home if no hash
        document.querySelector('.navbar__link[href="#home"]').classList.add('navbar__link--active');
    }
});
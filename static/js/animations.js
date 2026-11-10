/**
 * Trinails Portfolio Website - Animations & Scroll Reveal Controller
 * File: static/js/animations.js
 * Purpose: Controls the opening animated logo splash screen,
 *          scroll-triggered element reveals via IntersectionObserver,
 *          dynamic navbar blur on scroll, and scroll-spy active state.
 */

(function () {
    'use strict';

    /**
     * 1. Opening Logo Intro Animation Controller
     */
    function initIntroAnimation() {
        var loader = document.getElementById('site-intro-loader');
        if (!loader) {
            document.body.classList.add('site-ready');
            return;
        }

        // Check if intro has already been viewed in this session or arriving via hash anchor
        var hasSeenIntro = false;
        try {
            hasSeenIntro = sessionStorage.getItem('trinials_intro_seen') === 'true';
        } catch (e) {
            hasSeenIntro = false;
        }

        var isHashNav = !!(window.location.hash && window.location.hash.length > 1);

        if (hasSeenIntro || isHashNav) {
            // Instantly bypass intro preloader for maximum performance and fast LCP
            loader.classList.add('is-hidden');
            loader.setAttribute('aria-hidden', 'true');
            document.body.classList.remove('is-intro-active');
            document.body.classList.add('site-ready');
            setTimeout(function () {
                triggerInitialScrollReveals();
            }, 50);
            return;
        }

        // Mark as seen for subsequent pages and refreshes
        try {
            sessionStorage.setItem('trinials_intro_seen', 'true');
        } catch (e) {}

        // Add class to lock scroll during presentation
        document.body.classList.add('is-intro-active');

        var isFinished = false;
        var minDisplayDuration = 900; // Optimized duration for logo animation
        var startTime = performance.now();

        function finishIntro() {
            if (isFinished) return;
            isFinished = true;

            var elapsed = performance.now() - startTime;
            var remaining = Math.max(0, minDisplayDuration - elapsed);

            setTimeout(function () {
                loader.classList.add('is-leaving');
                document.body.classList.remove('is-intro-active');
                document.body.classList.add('site-ready');

                // Completely remove from rendering & accessibility tree after transition ends
                setTimeout(function () {
                    loader.classList.add('is-hidden');
                    loader.setAttribute('aria-hidden', 'true');
                    // Trigger initial scroll reveals for hero elements
                    triggerInitialScrollReveals();
                }, 500);
            }, remaining);
        }

        // Complete when window is fully loaded
        if (document.readyState === 'complete') {
            finishIntro();
        } else {
            window.addEventListener('load', finishIntro);
        }

        // Safety fallback timer: Guarantee site uncovers within 1.5 seconds maximum
        setTimeout(finishIntro, 1500);
    }

    /**
     * 2. Scroll-Triggered Reveal Animations via IntersectionObserver
     */
    function initScrollReveals() {
        // Elements automatically enhanced if not already annotated
        var autoTargets = [
            // About section
            { selector: '.about-badge, .about-heading, .about-lead, .about-body, .about-action', animation: 'reveal-fade-up' },
            { selector: '.about-visual', animation: 'reveal-scale' },
            // Services section
            { selector: '.services-header', animation: 'reveal-fade-up' },
            { selector: '.services-grid', animation: 'reveal-stagger-group' },
            // Work section
            { selector: '.work-header', animation: 'reveal-fade-up' },
            { selector: '.work-grid', animation: 'reveal-stagger-group' },
            // Process section
            { selector: '.process-header', animation: 'reveal-fade-up' },
            { selector: '.process-steps-grid', animation: 'reveal-stagger-group' },
            // Testimonials section
            { selector: '.testimonials-header', animation: 'reveal-fade-up' },
            { selector: '.testimonials-grid', animation: 'reveal-stagger-group' },
            // Contact section
            { selector: '.contact-content', animation: 'reveal-fade-left' },
            { selector: '.contact-form-wrapper', animation: 'reveal-fade-right' },
            // Footer
            { selector: '.footer-main', animation: 'reveal-fade-up' }
        ];

        autoTargets.forEach(function (target) {
            var elements = document.querySelectorAll(target.selector);
            elements.forEach(function (el) {
                if (!el.classList.contains('reveal-on-scroll') && 
                    !el.classList.contains('reveal-fade-up') &&
                    !el.classList.contains('reveal-fade-left') &&
                    !el.classList.contains('reveal-fade-right') &&
                    !el.classList.contains('reveal-scale') &&
                    !el.classList.contains('reveal-stagger-group')) {
                    el.classList.add(target.animation);
                }
            });
        });

        var revealElements = document.querySelectorAll(
            '.reveal-on-scroll, .reveal-fade-up, .reveal-fade-left, .reveal-fade-right, .reveal-scale, .reveal-stagger-group'
        );

        if (!revealElements.length) return;

        // Fallback for browsers or reduced motion preference
        var prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        if (!('IntersectionObserver' in window) || prefersReducedMotion) {
            revealElements.forEach(function (el) {
                el.classList.add('is-revealed');
            });
            return;
        }

        var observerOptions = {
            root: null,
            rootMargin: '0px 0px -60px 0px',
            threshold: 0.12
        };

        var observer = new IntersectionObserver(function (entries, obs) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('is-revealed');
                    obs.unobserve(entry.target);
                }
            });
        }, observerOptions);

        revealElements.forEach(function (el) {
            observer.observe(el);
        });
    }

    /**
     * Trigger reveals for any elements already visible on screen
     */
    function triggerInitialScrollReveals() {
        var viewportHeight = window.innerHeight || document.documentElement.clientHeight;
        var elements = document.querySelectorAll(
            '.reveal-on-scroll, .reveal-fade-up, .reveal-fade-left, .reveal-fade-right, .reveal-scale, .reveal-stagger-group'
        );

        elements.forEach(function (el) {
            var rect = el.getBoundingClientRect();
            if (rect.top <= viewportHeight * 0.85) {
                el.classList.add('is-revealed');
            }
        });
    }

    /**
     * 3. Sticky Header Scroll Enhancement
     */
    function initHeaderScrollState() {
        var header = document.getElementById('site-header');
        if (!header) return;

        function updateHeader() {
            if (window.scrollY > 24) {
                header.classList.add('is-scrolled');
            } else {
                header.classList.remove('is-scrolled');
            }
        }

        window.addEventListener('scroll', updateHeader, { passive: true });
        updateHeader();
    }

    /**
     * 4. Smooth Anchor Scrolling with Sticky Header Offset
     */
    function initSmoothAnchorScroll() {
        var links = document.querySelectorAll('a[href^="#"]');
        var header = document.getElementById('site-header');

        links.forEach(function (link) {
            link.addEventListener('click', function (e) {
                var targetId = this.getAttribute('href');
                if (targetId === '#' || targetId === '#top') {
                    e.preventDefault();
                    window.scrollTo({ top: 0, behavior: 'smooth' });
                    return;
                }

                var targetElement = document.querySelector(targetId);
                if (targetElement) {
                    e.preventDefault();
                    var headerOffset = header ? header.offsetHeight : 84;
                    var elementPosition = targetElement.getBoundingClientRect().top;
                    var offsetPosition = elementPosition + window.pageYOffset - headerOffset;

                    window.scrollTo({
                        top: offsetPosition,
                        behavior: 'smooth'
                    });
                }
            });
        });
    }

    /**
     * 5. Active Nav Link Scrollspy
     */
    function initScrollSpy() {
        var sections = document.querySelectorAll('section[id]');
        var navLinks = document.querySelectorAll('.navbar-desktop .nav-link, .navbar-mobile-panel .mobile-nav-link');
        var header = document.getElementById('site-header');

        if (!sections.length || !navLinks.length) return;

        function updateActiveLink() {
            var scrollPosition = window.pageYOffset + (header ? header.offsetHeight + 100 : 150);

            sections.forEach(function (section) {
                var sectionTop = section.offsetTop;
                var sectionHeight = section.offsetHeight;
                var sectionId = section.getAttribute('id');

                if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
                    navLinks.forEach(function (link) {
                        var href = link.getAttribute('href');
                        if (href === '#' + sectionId || (sectionId === 'hero' && (href === '/' || href === '#'))) {
                            link.classList.add('active');
                        } else if (href.indexOf('#' + sectionId) !== -1) {
                            link.classList.add('active');
                        } else if (href.startsWith('#')) {
                            link.classList.remove('active');
                        }
                    });
                }
            });
        }

        window.addEventListener('scroll', updateActiveLink, { passive: true });
        updateActiveLink();
    }

    /* Hero canvas interaction (tilt, focus areas, orb) lives in static/js/hero-canvas.js */

    // Initialize when DOM is parsed
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function () {
            initIntroAnimation();
            initScrollReveals();
            initHeaderScrollState();
            initSmoothAnchorScroll();
            initScrollSpy();
        });
    } else {
        initIntroAnimation();
        initScrollReveals();
        initHeaderScrollState();
        initSmoothAnchorScroll();
        initScrollSpy();
    }
})();


/**
 * Millennials Portfolio Website - Navigation Functionality
 * File: static/js/navigation.js
 * Purpose: Vanilla JS mobile navigation drawer toggle, accessibility (ARIA),
 *          outside click, Escape key handling, auto-close on link click,
 *          and "Let's Talk" contact dropdown interaction.
 */

(function () {
    'use strict';

    var closeMobileMenuFn = null;
    var closeAllContactDropdownsFn = null;

    function initNavigation() {
        var header = document.getElementById('site-header');
        var toggleBtn = document.getElementById('navbar-toggle');
        var menuPanel = document.getElementById('navbar-menu');

        // Graceful exit if elements do not exist on the current page
        if (!toggleBtn || !menuPanel) {
            return;
        }

        // Only standard mobile navigation links close the drawer directly
        var mobileLinks = menuPanel.querySelectorAll('.mobile-nav-link');

        /**
          * Open the mobile navigation panel
          */
        function openMenu() {
            // Close any open contact dropdowns so the drawer has full clarity
            if (typeof closeAllContactDropdownsFn === 'function') {
                closeAllContactDropdownsFn(false);
            }

            toggleBtn.setAttribute('aria-expanded', 'true');
            menuPanel.setAttribute('aria-hidden', 'false');
            toggleBtn.classList.add('is-active');
            menuPanel.classList.add('is-open');
        }

        /**
          * Close the mobile navigation panel
          */
        function closeMenu(restoreFocus) {
            toggleBtn.setAttribute('aria-expanded', 'false');
            menuPanel.setAttribute('aria-hidden', 'true');
            toggleBtn.classList.remove('is-active');
            menuPanel.classList.remove('is-open');

            if (restoreFocus && typeof toggleBtn.focus === 'function') {
                toggleBtn.focus();
            }
        }

        closeMobileMenuFn = closeMenu;

        /**
          * Toggle menu state
          */
        function toggleMenu() {
            var isExpanded = toggleBtn.getAttribute('aria-expanded') === 'true';
            if (isExpanded) {
                closeMenu(false);
            } else {
                openMenu();
            }
        }

        // 1. Toggle button click event
        toggleBtn.addEventListener('click', function (event) {
            event.stopPropagation();
            toggleMenu();
        });

        // 2. Close menu on clicking any standard navigation link
        mobileLinks.forEach(function (link) {
            link.addEventListener('click', function () {
                closeMenu(false);
            });
        });

        // 3. Close menu when clicking outside of the header
        document.addEventListener('click', function (event) {
            var isExpanded = toggleBtn.getAttribute('aria-expanded') === 'true';
            if (isExpanded && header && !header.contains(event.target)) {
                closeMenu(false);
            }
        });

        // 4. Close menu when pressing Escape key (and return focus to toggle button)
        document.addEventListener('keydown', function (event) {
            if (event.key === 'Escape' || event.keyCode === 27) {
                var isExpanded = toggleBtn.getAttribute('aria-expanded') === 'true';
                if (isExpanded) {
                    closeMenu(true);
                }
            }
        });

        // 5. Automatically close menu if viewport is resized back to desktop (>768px)
        window.addEventListener('resize', function () {
            if (window.innerWidth > 768) {
                var isExpanded = toggleBtn.getAttribute('aria-expanded') === 'true';
                if (isExpanded) {
                    closeMenu(false);
                }
            }
        });
    }

    /**
     * Initialize "Let's Talk" contact dropdown interaction (Desktop & Mobile)
     */
    function initContactDropdowns() {
        var dropdownConfigs = [
            {
                triggerId: 'nav-cta-trigger',
                dropdownId: 'nav-contact-dropdown'
            },
            {
                // Fallback config in case mobile-nav-cta-trigger is referenced
                triggerId: 'mobile-nav-cta-trigger',
                dropdownId: 'mobile-nav-contact-dropdown'
            }
        ];

        var instances = [];

        dropdownConfigs.forEach(function (config) {
            var trigger = document.getElementById(config.triggerId);
            var dropdown = document.getElementById(config.dropdownId);

            if (!trigger || !dropdown) return;

            var wrapper = trigger.closest('.nav-dropdown-wrapper') || trigger.parentElement;
            var items = dropdown.querySelectorAll('.nav-contact-item');

            function openDropdown() {
                // If mobile navigation drawer is open, close it so contact dropdown is front and center
                if (typeof closeMobileMenuFn === 'function') {
                    closeMobileMenuFn(false);
                }

                // Close any other open dropdowns first
                instances.forEach(function (inst) {
                    if (inst.trigger !== trigger && inst.isOpen()) {
                        inst.close(false);
                    }
                });

                trigger.setAttribute('aria-expanded', 'true');
                dropdown.setAttribute('aria-hidden', 'false');
                trigger.classList.add('is-active');
                dropdown.classList.add('is-open');
            }

            function closeDropdown(restoreFocus) {
                var wasOpen = trigger.getAttribute('aria-expanded') === 'true';
                trigger.setAttribute('aria-expanded', 'false');
                dropdown.setAttribute('aria-hidden', 'true');
                trigger.classList.remove('is-active');
                dropdown.classList.remove('is-open');

                if (restoreFocus && wasOpen && typeof trigger.focus === 'function') {
                    trigger.focus();
                }
            }

            function toggleDropdown() {
                var isExpanded = trigger.getAttribute('aria-expanded') === 'true';
                if (isExpanded) {
                    closeDropdown(false);
                } else {
                    openDropdown();
                }
            }

            var lastTouchTime = 0;

            // Handle touch taps directly (bypasses mobile Safari hover trap and eliminates 300ms tap delay)
            trigger.addEventListener('touchend', function (event) {
                // Ignore multi-touch pinches/gestures
                if (event.touches && event.touches.length > 0) return;

                lastTouchTime = Date.now();
                event.preventDefault(); // Prevents mobile browsers from synthesizing a duplicate click 300ms later
                event.stopPropagation();
                toggleDropdown();
            }, { passive: false });

            // Handle standard mouse click (desktop and fallback)
            trigger.addEventListener('click', function (event) {
                // Ignore synthetic clicks fired immediately after touchend
                if (Date.now() - lastTouchTime < 500) {
                    event.preventDefault();
                    event.stopPropagation();
                    return;
                }
                event.preventDefault();
                event.stopPropagation();
                toggleDropdown();
            });

            // Prevent touch and pointer events inside wrapper from bubbling to document outside-close handlers
            if (wrapper) {
                wrapper.addEventListener('touchend', function (event) {
                    event.stopPropagation();
                }, { passive: false });
                wrapper.addEventListener('pointerdown', function (event) {
                    event.stopPropagation();
                });
            }

            // Click contact item: allow native navigation to trigger, then close
            items.forEach(function (item) {
                item.addEventListener('click', function () {
                    setTimeout(function () {
                        closeDropdown(false);
                    }, 120);
                });
                item.addEventListener('touchend', function () {
                    setTimeout(function () {
                        closeDropdown(false);
                    }, 120);
                }, { passive: true });
            });

            // Keyboard accessibility: close if keyboard focus moves completely outside wrapper
            if (wrapper) {
                wrapper.addEventListener('focusout', function (event) {
                    // Only close if focus explicitly moved to an element outside the wrapper (keyboard tab navigation)
                    if (event.relatedTarget && !wrapper.contains(event.relatedTarget)) {
                        closeDropdown(false);
                    }
                });
            }

            instances.push({
                trigger: trigger,
                dropdown: dropdown,
                wrapper: wrapper,
                close: closeDropdown,
                isOpen: function () {
                    return trigger.getAttribute('aria-expanded') === 'true';
                }
            });
        });

        if (instances.length === 0) return;

        closeAllContactDropdownsFn = function (restoreFocus) {
            instances.forEach(function (inst) {
                if (inst.isOpen()) {
                    inst.close(restoreFocus);
                }
            });
        };

        // Close dropdown when clicking or tapping outside
        function handleOutsideInteraction(event) {
            instances.forEach(function (inst) {
                if (inst.isOpen()) {
                    if (inst.wrapper && !inst.wrapper.contains(event.target)) {
                        inst.close(false);
                    }
                }
            });
        }

        document.addEventListener('click', handleOutsideInteraction);
        document.addEventListener('touchend', function (event) {
            instances.forEach(function (inst) {
                if (inst.isOpen()) {
                    if (inst.wrapper && !inst.wrapper.contains(event.target)) {
                        inst.close(false);
                    }
                }
            });
        }, { passive: true });
        document.addEventListener('pointerdown', function (event) {
            instances.forEach(function (inst) {
                if (inst.isOpen()) {
                    if (inst.wrapper && !inst.wrapper.contains(event.target)) {
                        inst.close(false);
                    }
                }
            });
        });

        // Close dropdown on Escape key and return focus to trigger button
        document.addEventListener('keydown', function (event) {
            if (event.key === 'Escape' || event.keyCode === 27) {
                var closedAny = false;
                instances.forEach(function (inst) {
                    if (inst.isOpen()) {
                        inst.close(true);
                        closedAny = true;
                    }
                });
                if (closedAny) {
                    event.stopPropagation();
                }
            }
        });

        // Close dropdown on genuine window width resize (orientation change or desktop resize)
        var lastViewportWidth = window.innerWidth;
        window.addEventListener('resize', function () {
            if (window.innerWidth === lastViewportWidth) {
                return; // Ignore mobile height-only changes caused by address bar show/hide
            }
            lastViewportWidth = window.innerWidth;
            instances.forEach(function (inst) {
                if (inst.isOpen()) {
                    inst.close(false);
                }
            });
        });
    }

    function initContactForm() {
        var form = document.getElementById('contact-form');
        if (!form) return;

        form.addEventListener('submit', function () {
            if (form.checkValidity && !form.checkValidity()) {
                return;
            }
            var btn = form.querySelector('.contact-btn-submit');
            if (btn && !btn.disabled) {
                setTimeout(function () {
                    btn.disabled = true;
                    btn.classList.add('is-submitting');
                }, 50);

                setTimeout(function () {
                    btn.disabled = false;
                    btn.classList.remove('is-submitting');
                }, 8000);
            }
        });
    }

    function initAll() {
        initNavigation();
        initContactDropdowns();
        initContactForm();
    }

    // Initialize once DOM is fully loaded
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initAll);
    } else {
        initAll();
    }
})();

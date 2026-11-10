/**
 * Trinails Portfolio Website - Hero Visual Canvas Controller
 * File: static/js/hero-canvas.js
 * Purpose: Makes the hero canvas (.visual-canvas) interactive:
 *   1. Depth tilt   - the glass card, rings, orb and badges follow the pointer
 *                     at different distances, with a glass highlight under it.
 *   2. Focus areas  - the three chips under the hero buttons (and the orb)
 *                     switch the canvas between Strategic Design, Modern
 *                     Engineering and Enduring Craft: badge copy, icon, orb
 *                     tint, ring scale and horizon line all change together.
 *   3. Orb          - clicking it releases a pulse and shows the next focus area.
 *   4. Auto-cycle   - the focus areas rotate slowly until the visitor takes over.
 *
 * Accessibility: real <button> controls, aria-pressed state, a polite live
 * region for visitor-made changes, and prefers-reduced-motion is respected
 * (no tilt, no pulse, no auto-cycle).
 */

(function () {
    'use strict';

    var SCENES = [
        {
            id: 'design',
            pill: 'Thoughtful Strategy',
            title: 'Original Ideas',
            sub: 'Crafted with purpose',
            announce: 'Strategic Design: thoughtful strategy and original ideas, crafted with purpose.'
        },
        {
            id: 'engineering',
            pill: 'Clean Engineering',
            title: 'Built to Scale',
            sub: 'Engineered for growth',
            announce: 'Modern Engineering: clean engineering, built to scale and engineered for growth.'
        },
        {
            id: 'craft',
            pill: 'Lasting Quality',
            title: 'Made to Last',
            sub: 'Care in every detail',
            announce: 'Enduring Craft: lasting quality, made to last with care in every detail.'
        }
    ];

    var AUTO_INTERVAL_MS = 7000;
    var SWAP_MS = 160;
    var TILT_EASE = 0.12;

    function initHeroCanvas() {
        var section = document.getElementById('hero');
        var visual = document.getElementById('hero-visual');
        var canvas = document.getElementById('hero-canvas');
        var orb = document.getElementById('hero-orb');
        if (!section || !visual || !canvas || !orb) return;

        var pillText = document.getElementById('hero-pill-text');
        var cardTitle = document.getElementById('hero-card-title');
        var cardSub = document.getElementById('hero-card-sub');
        var live = document.getElementById('hero-live');
        var chips = Array.prototype.slice.call(section.querySelectorAll('.hero-meta-item[data-scene]'));
        var meta = section.querySelector('.hero-meta');

        var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
        var finePointer = window.matchMedia('(hover: hover) and (pointer: fine)');

        var current = 0;
        var visitorTookOver = false;
        var hovering = false;
        var focusInside = false;
        var inView = true;
        var autoTimer = null;
        var swapTimer = null;

        /* ---------------------------------------------------------------
           Focus areas
           --------------------------------------------------------------- */
        function applyCopy() {
            var scene = SCENES[current];
            if (pillText) pillText.textContent = scene.pill;
            if (cardTitle) cardTitle.textContent = scene.title;
            if (cardSub) cardSub.textContent = scene.sub;
        }

        function setScene(index, fromVisitor) {
            index = (index + SCENES.length) % SCENES.length;
            if (index === current) return;
            current = index;
            var scene = SCENES[current];

            visual.setAttribute('data-scene', scene.id);

            chips.forEach(function (chip) {
                var active = chip.getAttribute('data-scene') === scene.id;
                chip.setAttribute('aria-pressed', active ? 'true' : 'false');
                chip.classList.toggle('is-active', active);
            });

            // Fade the copy out, swap it, fade it back in
            if (reduceMotion.matches) {
                applyCopy();
            } else {
                visual.classList.add('is-swapping');
                clearTimeout(swapTimer);
                swapTimer = setTimeout(function () {
                    applyCopy();
                    visual.classList.remove('is-swapping');
                }, SWAP_MS);
            }

            if (fromVisitor && live) live.textContent = scene.announce;
        }

        function sceneIndexById(id) {
            for (var i = 0; i < SCENES.length; i++) {
                if (SCENES[i].id === id) return i;
            }
            return 0;
        }

        function takeOver() {
            visitorTookOver = true;
            stopAuto();
        }

        chips.forEach(function (chip, i) {
            chip.addEventListener('click', function () {
                takeOver();
                setScene(sceneIndexById(chip.getAttribute('data-scene')), true);
            });

            // Arrow keys move between the three switches
            chip.addEventListener('keydown', function (e) {
                var step = 0;
                if (e.key === 'ArrowRight' || e.key === 'ArrowDown') step = 1;
                if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') step = -1;
                if (!step) return;
                e.preventDefault();
                var next = chips[(i + step + chips.length) % chips.length];
                next.focus();
                takeOver();
                setScene(sceneIndexById(next.getAttribute('data-scene')), true);
            });
        });

        /* ---------------------------------------------------------------
           Orb: pulse + next focus area
           --------------------------------------------------------------- */
        function pulse() {
            if (reduceMotion.matches) return;
            var ring = document.createElement('span');
            ring.className = 'visual-pulse';
            ring.setAttribute('aria-hidden', 'true');
            orb.parentNode.appendChild(ring);
            ring.addEventListener('animationend', function () {
                if (ring.parentNode) ring.parentNode.removeChild(ring);
            });
        }

        orb.addEventListener('click', function () {
            takeOver();
            pulse();
            setScene(current + 1, true);
        });

        /* ---------------------------------------------------------------
           Pointer tilt (mouse and pen only, never touch)
           --------------------------------------------------------------- */
        var targetX = 0;
        var targetY = 0;
        var currentX = 0;
        var currentY = 0;
        var frameId = 0;
        var lastTime = 0;

        function clamp(v) {
            return Math.max(-1, Math.min(1, v));
        }

        function paint() {
            visual.style.setProperty('--px', currentX.toFixed(3));
            visual.style.setProperty('--py', currentY.toFixed(3));
        }

        function step(now) {
            // Ease by elapsed time so the motion feels the same at 30, 60 or 144 Hz
            var dt = lastTime ? Math.min(now - lastTime, 64) : 16.7;
            lastTime = now;
            var k = 1 - Math.pow(1 - TILT_EASE, dt / 16.7);
            currentX += (targetX - currentX) * k;
            currentY += (targetY - currentY) * k;

            if (Math.abs(targetX - currentX) < 0.002 && Math.abs(targetY - currentY) < 0.002) {
                currentX = targetX;
                currentY = targetY;
                paint();
                frameId = 0;
                lastTime = 0;
                return;
            }
            paint();
            frameId = requestAnimationFrame(step);
        }

        function kick() {
            if (!frameId) frameId = requestAnimationFrame(step);
        }

        function tiltAllowed() {
            return finePointer.matches && !reduceMotion.matches;
        }

        visual.addEventListener('pointermove', function (e) {
            if (e.pointerType === 'touch' || !tiltAllowed()) return;

            var box = visual.getBoundingClientRect();
            var halfW = (canvas.offsetWidth || box.width) / 2;
            var halfH = (canvas.offsetHeight || box.height) / 2;
            var left = box.left + canvas.offsetLeft;
            var top = box.top + canvas.offsetTop;

            targetX = clamp((e.clientX - (left + halfW)) / (halfW * 1.15));
            targetY = clamp((e.clientY - (top + halfH)) / (halfH * 1.15));

            // Position of the glass highlight, in % of the canvas
            visual.style.setProperty('--mx', (((e.clientX - left) / (halfW * 2)) * 100).toFixed(1) + '%');
            visual.style.setProperty('--my', (((e.clientY - top) / (halfH * 2)) * 100).toFixed(1) + '%');

            visual.classList.add('is-active');
            kick();
        });

        visual.addEventListener('pointerleave', function () {
            targetX = 0;
            targetY = 0;
            visual.classList.remove('is-active');
            kick();
        });

        /* ---------------------------------------------------------------
           Auto-cycle until the visitor interacts
           --------------------------------------------------------------- */
        function autoTick() {
            if (document.hidden || hovering || focusInside || !inView) return;
            if (document.body.classList.contains('is-intro-active')) return;
            setScene(current + 1, false);
        }

        function startAuto() {
            if (autoTimer || visitorTookOver || reduceMotion.matches) return;
            autoTimer = setInterval(autoTick, AUTO_INTERVAL_MS);
        }

        function stopAuto() {
            clearInterval(autoTimer);
            autoTimer = null;
        }

        // Pause while the visitor is looking at, or navigating, the hero controls
        [visual, meta].forEach(function (el) {
            if (!el) return;
            el.addEventListener('pointerenter', function () { hovering = true; });
            el.addEventListener('pointerleave', function () { hovering = false; });
        });

        section.addEventListener('focusin', function (e) {
            if (visual.contains(e.target) || (meta && meta.contains(e.target))) focusInside = true;
        });
        section.addEventListener('focusout', function () { focusInside = false; });

        if ('IntersectionObserver' in window) {
            new IntersectionObserver(function (entries) {
                inView = entries[0].isIntersecting;
            }, { threshold: 0.25 }).observe(section);
        }

        if (reduceMotion.addEventListener) {
            reduceMotion.addEventListener('change', function () {
                if (reduceMotion.matches) {
                    stopAuto();
                    targetX = 0;
                    targetY = 0;
                    kick();
                } else {
                    startAuto();
                }
            });
        }

        startAuto();
    }

    function initAboutCanvas() {
        var visual = document.getElementById('about-visual');
        var canvas = document.getElementById('about-canvas');
        var orb = document.getElementById('about-orb');
        if (!visual || !canvas) return;

        var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
        var finePointer = window.matchMedia('(hover: hover) and (pointer: fine)');

        var targetX = 0;
        var targetY = 0;
        var currentX = 0;
        var currentY = 0;
        var frameId = 0;
        var lastTime = 0;

        function clamp(v) {
            return Math.max(-1, Math.min(1, v));
        }

        function paint() {
            visual.style.setProperty('--px', currentX.toFixed(3));
            visual.style.setProperty('--py', currentY.toFixed(3));
        }

        function step(now) {
            var dt = lastTime ? Math.min(now - lastTime, 64) : 16.7;
            lastTime = now;
            var k = 1 - Math.pow(1 - TILT_EASE, dt / 16.7);
            currentX += (targetX - currentX) * k;
            currentY += (targetY - currentY) * k;

            if (Math.abs(targetX - currentX) < 0.002 && Math.abs(targetY - currentY) < 0.002) {
                currentX = targetX;
                currentY = targetY;
                paint();
                frameId = 0;
                lastTime = 0;
                return;
            }
            paint();
            frameId = requestAnimationFrame(step);
        }

        function kick() {
            if (!frameId) frameId = requestAnimationFrame(step);
        }

        function tiltAllowed() {
            return finePointer.matches && !reduceMotion.matches;
        }

        visual.addEventListener('pointermove', function (e) {
            if (e.pointerType === 'touch' || !tiltAllowed()) return;

            var box = visual.getBoundingClientRect();
            var halfW = (canvas.offsetWidth || box.width) / 2;
            var halfH = (canvas.offsetHeight || box.height) / 2;
            var left = box.left + canvas.offsetLeft;
            var top = box.top + canvas.offsetTop;

            targetX = clamp((e.clientX - (left + halfW)) / (halfW * 1.15));
            targetY = clamp((e.clientY - (top + halfH)) / (halfH * 1.15));

            visual.style.setProperty('--mx', (((e.clientX - left) / (halfW * 2)) * 100).toFixed(1) + '%');
            visual.style.setProperty('--my', (((e.clientY - top) / (halfH * 2)) * 100).toFixed(1) + '%');

            visual.classList.add('is-active');
            kick();
        });

        visual.addEventListener('pointerleave', function () {
            targetX = 0;
            targetY = 0;
            visual.classList.remove('is-active');
            kick();
        });

        if (orb) {
            orb.addEventListener('click', function () {
                if (reduceMotion.matches) return;
                var pulseRing = document.createElement('span');
                pulseRing.className = 'visual-pulse';
                pulseRing.style.borderColor = 'rgba(88, 100, 29, 0.55)';
                pulseRing.setAttribute('aria-hidden', 'true');
                orb.parentNode.appendChild(pulseRing);
                pulseRing.addEventListener('animationend', function () {
                    if (pulseRing.parentNode) pulseRing.parentNode.removeChild(pulseRing);
                });
            });
        }
    }

    function initAllCanvases() {
        initHeroCanvas();
        initAboutCanvas();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initAllCanvases);
    } else {
        initAllCanvases();
    }
})();

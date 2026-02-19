/**
 * hamburger.js — Standalone mobile hamburger menu
 * Works on ANY page (land, about, pair pages, etc.)
 * Does NOT require converters.js or app.js.
 */
(function () {
    'use strict';

    function buildHamburgerMenu() {
        const headerInner = document.querySelector('.header-inner');
        if (!headerInner || document.getElementById('hamburger-btn')) return;

        // ── Hamburger button ──
        const btn = document.createElement('button');
        btn.id = 'hamburger-btn';
        btn.className = 'hamburger-btn';
        btn.setAttribute('aria-label', 'Open menu');
        btn.setAttribute('aria-expanded', 'false');
        btn.innerHTML = '<span></span><span></span><span></span>';
        headerInner.appendChild(btn);

        // ── Slide-in drawer ──
        const drawer = document.createElement('nav');
        drawer.id = 'mobile-drawer';
        drawer.className = 'mobile-drawer';
        drawer.setAttribute('aria-label', 'Mobile navigation');
        drawer.innerHTML = `
          <div class="drawer-header">
            <span class="drawer-title">Converters</span>
            <button class="drawer-close" id="drawer-close" aria-label="Close menu">✕</button>
          </div>
          <div class="drawer-links"></div>
        `;

        // Populate from existing .site-nav links
        const drawerLinks = drawer.querySelector('.drawer-links');
        document.querySelectorAll('.site-nav .nav-link').forEach(link => {
            const a = link.cloneNode(true);
            a.classList.add('drawer-link');
            drawerLinks.appendChild(a);
        });

        // ── Overlay ──
        const overlay = document.createElement('div');
        overlay.id = 'drawer-overlay';
        overlay.className = 'drawer-overlay';

        document.body.appendChild(drawer);
        document.body.appendChild(overlay);

        function openDrawer() {
            drawer.classList.add('open');
            overlay.classList.add('open');
            btn.classList.add('open');
            btn.setAttribute('aria-expanded', 'true');
            document.body.style.overflow = 'hidden';
        }
        function closeDrawer() {
            drawer.classList.remove('open');
            overlay.classList.remove('open');
            btn.classList.remove('open');
            btn.setAttribute('aria-expanded', 'false');
            document.body.style.overflow = '';
        }

        btn.addEventListener('click', () =>
            drawer.classList.contains('open') ? closeDrawer() : openDrawer()
        );
        document.getElementById('drawer-close').addEventListener('click', closeDrawer);
        overlay.addEventListener('click', closeDrawer);
        drawerLinks.querySelectorAll('.drawer-link').forEach(a =>
            a.addEventListener('click', closeDrawer)
        );
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', buildHamburgerMenu);
    } else {
        buildHamburgerMenu();
    }
})();

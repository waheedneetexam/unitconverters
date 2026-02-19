/**
 * app.js — UI Logic for SwapUnits.online
 * Handles tab switching, real-time conversion, swap, copy
 * + Mobile: hamburger menu, dropdown selects
 */

(function () {
    'use strict';

    // ── State ──
    let currentCategory = 'length';
    const MOBILE_BP = 768; // px — below this = mobile behaviour

    // ── DOM refs ──
    const tabsContainer = document.getElementById('category-tabs');
    const converterBody = document.getElementById('converter-body');
    const pageTitle = document.getElementById('page-title');
    const pageTitleH1 = document.getElementById('converter-title');

    // ── Mobile detection ──
    function isMobile() {
        return window.innerWidth <= MOBILE_BP;
    }

    // ─────────────────────────────────────────────
    //  HAMBURGER MENU
    // ─────────────────────────────────────────────
    function buildHamburgerMenu() {
        const headerInner = document.querySelector('.header-inner');
        if (!headerInner || document.getElementById('hamburger-btn')) return;

        // Hamburger button
        const btn = document.createElement('button');
        btn.id = 'hamburger-btn';
        btn.className = 'hamburger-btn';
        btn.setAttribute('aria-label', 'Open menu');
        btn.setAttribute('aria-expanded', 'false');
        btn.innerHTML = '<span></span><span></span><span></span>';
        headerInner.appendChild(btn);

        // Slide-in drawer
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

        // Populate drawer from existing nav links
        const navLinks = document.querySelectorAll('.site-nav .nav-link');
        const drawerLinks = drawer.querySelector('.drawer-links');
        navLinks.forEach(link => {
            const a = link.cloneNode(true);
            a.classList.add('drawer-link');
            drawerLinks.appendChild(a);
        });

        // Dim overlay
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

        btn.addEventListener('click', () => {
            drawer.classList.contains('open') ? closeDrawer() : openDrawer();
        });
        document.getElementById('drawer-close').addEventListener('click', closeDrawer);
        overlay.addEventListener('click', closeDrawer);
        drawerLinks.querySelectorAll('.drawer-link').forEach(a => {
            a.addEventListener('click', closeDrawer);
        });
    }

    // ── Build tabs ──
    function buildTabs() {
        if (!tabsContainer) return;
        tabsContainer.innerHTML = '';
        Object.entries(CONVERTERS).forEach(([key, cat]) => {
            const btn = document.createElement('button');
            btn.className = 'cat-tab' + (key === currentCategory ? ' active' : '');
            btn.textContent = cat.name;
            btn.setAttribute('data-category', key);
            btn.setAttribute('aria-label', cat.name + ' converter');
            btn.addEventListener('click', () => switchCategory(key));
            tabsContainer.appendChild(btn);
        });
    }

    // ── Build converter UI ──
    function buildConverter(categoryKey) {
        const cat = CONVERTERS[categoryKey];
        if (!cat || !converterBody) return;

        if (pageTitleH1) pageTitleH1.textContent = cat.name + ' Converter';
        if (pageTitle) document.title = cat.name + ' Converter — SwapUnits.online';

        const iconEl = document.querySelector('.calc-icon');
        if (iconEl && cat.icon) iconEl.textContent = cat.icon;

        const defaultFrom = cat.units[0].id;
        const defaultTo = cat.units[1] ? cat.units[1].id : cat.units[0].id;

        // On mobile use size=1 (compact dropdown), on desktop use size=8 (listbox)
        const selectSize = isMobile() ? '1' : '8';

        converterBody.innerHTML = `
      <div class="converter-grid">
        <div class="converter-field">
          <label for="from-value">From</label>
          <input type="number" id="from-value" placeholder="Enter value" value="1" autocomplete="off" />
          <select id="from-unit" size="${selectSize}" aria-label="From unit">
            ${cat.units.map(u => `<option value="${u.id}"${u.id === defaultFrom ? ' selected' : ''}>${u.label}</option>`).join('')}
          </select>
        </div>
        <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;">
          <button class="swap-btn" id="swap-btn" title="Swap units" aria-label="Swap from and to units">⇄</button>
        </div>
        <div class="converter-field">
          <label for="to-value">To</label>
          <input type="text" id="to-value" placeholder="Result" readonly tabindex="-1" />
          <select id="to-unit" size="${selectSize}" aria-label="To unit">
            ${cat.units.map(u => `<option value="${u.id}"${u.id === defaultTo ? ' selected' : ''}>${u.label}</option>`).join('')}
          </select>
        </div>
      </div>
      <div class="result-display" id="result-display">
        <div>
          <div class="result-text" id="result-label">Result</div>
          <div class="result-value" id="result-value">—</div>
        </div>
        <button class="copy-btn" id="copy-btn" aria-label="Copy result">📋 Copy</button>
      </div>
    `;

        const fromVal = document.getElementById('from-value');
        const fromUnit = document.getElementById('from-unit');
        const toVal = document.getElementById('to-value');
        const toUnit = document.getElementById('to-unit');
        const swapBtn = document.getElementById('swap-btn');
        const copyBtn = document.getElementById('copy-btn');
        const resultEl = document.getElementById('result-value');
        const labelEl = document.getElementById('result-label');

        fromUnit.value = defaultFrom;
        toUnit.value = defaultTo;

        function doConvert() {
            const val = parseFloat(fromVal.value);
            const from = fromUnit.value || defaultFrom;
            const to = toUnit.value || defaultTo;
            if (isNaN(val)) { resultEl.textContent = '\u2014'; toVal.value = ''; return; }
            const result = cat.convert(val, from, to);
            const formatted = formatResult(result);
            toVal.value = (formatted === '\u2014') ? '' : formatted;
            resultEl.textContent = formatted;
            const fromLabel = cat.units.find(u => u.id === from)?.label || from;
            const toLabel = cat.units.find(u => u.id === to)?.label || to;
            labelEl.textContent = `${val} ${fromLabel} =`;
        }

        fromVal.addEventListener('input', doConvert);
        fromUnit.addEventListener('change', doConvert);
        toUnit.addEventListener('change', doConvert);

        swapBtn.addEventListener('click', () => {
            const tmp = fromUnit.value;
            fromUnit.value = toUnit.value;
            toUnit.value = tmp;
            doConvert();
        });

        copyBtn.addEventListener('click', () => {
            const text = resultEl.textContent;
            if (text && text !== '—') {
                navigator.clipboard.writeText(text).then(() => {
                    copyBtn.textContent = '✅ Copied!';
                    setTimeout(() => { copyBtn.textContent = '📋 Copy'; }, 1800);
                });
            }
        });

        doConvert();
        buildQuickRef(categoryKey);
    }

    // ── Quick Reference Table ──
    function buildQuickRef(categoryKey) {
        const tableBody = document.getElementById('quick-ref-body');
        if (!tableBody) return;
        const cat = CONVERTERS[categoryKey];
        const baseUnit = cat.units[0];
        const rows = cat.units.slice(1, 9).map(u => {
            const result = cat.convert(1, baseUnit.id, u.id);
            return `<tr>
        <td>1 ${baseUnit.label}</td>
        <td>${formatResult(result)} ${u.label}</td>
      </tr>`;
        });
        tableBody.innerHTML = rows.join('');
        const refTitle = document.getElementById('quick-ref-title');
        if (refTitle) refTitle.textContent = `Quick Reference — ${cat.name}`;
    }

    // ── Switch category ──
    function switchCategory(key) {
        currentCategory = key;
        document.querySelectorAll('.cat-tab').forEach(btn => {
            btn.classList.toggle('active', btn.getAttribute('data-category') === key);
        });
        buildConverter(key);
        // Update both top nav and drawer links
        document.querySelectorAll('.nav-link, .drawer-link').forEach(link => {
            link.classList.toggle('active', link.getAttribute('data-category') === key);
        });
    }

    // ── Popular conversions click ──
    function bindPopularItems() {
        document.querySelectorAll('.popular-item').forEach(item => {
            item.addEventListener('click', () => {
                const cat = item.getAttribute('data-cat');
                const from = item.getAttribute('data-from');
                const to = item.getAttribute('data-to');
                if (cat && from && to) {
                    switchCategory(cat);
                    setTimeout(() => {
                        const fromUnit = document.getElementById('from-unit');
                        const toUnit = document.getElementById('to-unit');
                        if (fromUnit) fromUnit.value = from;
                        if (toUnit) toUnit.value = to;
                        const fromVal = document.getElementById('from-value');
                        if (fromVal) fromVal.value = '1';
                        const cat_obj = CONVERTERS[cat];
                        if (cat_obj) {
                            const result = cat_obj.convert(1, from, to);
                            const resultEl = document.getElementById('result-value');
                            const toVal = document.getElementById('to-value');
                            if (resultEl) resultEl.textContent = formatResult(result);
                            if (toVal) toVal.value = formatResult(result);
                        }
                    }, 50);
                }
            });
        });
    }

    // ── Init ──
    function init() {
        const bodyCategory = document.body.getAttribute('data-category');
        if (bodyCategory && CONVERTERS[bodyCategory]) {
            currentCategory = bodyCategory;
        }

        buildHamburgerMenu();
        buildTabs();
        buildConverter(currentCategory);
        bindPopularItems();

        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.toggle('active', link.getAttribute('data-category') === currentCategory);
        });

        // Rebuild on resize so select size updates correctly
        let resizeTimer;
        window.addEventListener('resize', () => {
            clearTimeout(resizeTimer);
            resizeTimer = setTimeout(() => buildConverter(currentCategory), 150);
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();

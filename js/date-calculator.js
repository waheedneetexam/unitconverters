/**
 * date-calculator.js
 * Logic for the Date Calculator page
 */

(function () {
    'use strict';

    // ── Helper Functions ──

    function isValidDate(d, m, y) {
        const date = new Date(y, m - 1, d);
        return date.getFullYear() === y && date.getMonth() === m - 1 && date.getDate() === d;
    }

    function formatDateForPicker(d, m, y) {
        // yyyy-mm-dd
        return `${y}-${String(m).padStart(2, '0')}-${String(d).padStart(2, '0')}`;
    }

    function parseDateFromPicker(val) {
        // val is yyyy-mm-dd
        const parts = val.split('-');
        return {
            year: parseInt(parts[0], 10),
            month: parseInt(parts[1], 10),
            day: parseInt(parts[2], 10)
        };
    }

    function setDateInputs(prefix, d, m, y) {
        const dayInput = document.getElementById(`${prefix}-day`);
        const monthInput = document.getElementById(`${prefix}-month`);
        const yearInput = document.getElementById(`${prefix}-year`);
        const picker = document.getElementById(`${prefix}-date-picker`);

        if (dayInput) dayInput.value = d;
        if (monthInput) monthInput.value = m;
        if (yearInput) yearInput.value = y;
        if (picker) picker.value = formatDateForPicker(d, m, y);
    }

    function getDateFromInputs(prefix) {
        const d = parseInt(document.getElementById(`${prefix}-day`).value, 10);
        const m = parseInt(document.getElementById(`${prefix}-month`).value, 10);
        const y = parseInt(document.getElementById(`${prefix}-year`).value, 10);
        return { d, m, y };
    }

    function syncPickerToInputs(prefix) {
        const { d, m, y } = getDateFromInputs(prefix);
        if (d && m && y && isValidDate(d, m, y)) {
            document.getElementById(`${prefix}-date-picker`).value = formatDateForPicker(d, m, y);
        }
    }

    function syncInputsToPicker(prefix) {
        const val = document.getElementById(`${prefix}-date-picker`).value;
        if (val) {
            const date = parseDateFromPicker(val);
            document.getElementById(`${prefix}-day`).value = date.day;
            document.getElementById(`${prefix}-month`).value = date.month;
            document.getElementById(`${prefix}-year`).value = date.year;
        }
    }

    function setToday(prefix) {
        const now = new Date();
        setDateInputs(prefix, now.getDate(), now.getMonth() + 1, now.getFullYear());
    }

    function setupDateListeners(prefix) {
        const day = document.getElementById(`${prefix}-day`);
        const month = document.getElementById(`${prefix}-month`);
        const year = document.getElementById(`${prefix}-year`);
        const picker = document.getElementById(`${prefix}-date-picker`);
        const trigger = document.getElementById(`${prefix}-picker-trigger`);
        const todayBtn = document.getElementById(`${prefix}-today-btn`);

        if (day && month && year) {
            [day, month, year].forEach(el => {
                el.addEventListener('input', () => syncPickerToInputs(prefix));
            });
        }

        if (picker) {
            picker.addEventListener('change', () => syncInputsToPicker(prefix));
        }

        if (trigger && picker) {
            trigger.addEventListener('click', () => picker.showPicker());
        }

        if (todayBtn) {
            todayBtn.addEventListener('click', (e) => {
                e.preventDefault();
                setToday(prefix);
            });
        }
    }

    // ── Tab Logic ──
    const tabs = document.querySelectorAll('.date-calc-tab');
    const tabContents = document.querySelectorAll('.tab-content');
    const resultSection = document.getElementById('result-section');

    tabs.forEach(tab => {
        tab.addEventListener('click', (e) => {
            e.preventDefault();

            // Remove active class from all tabs
            tabs.forEach(t => t.classList.remove('active'));
            // Add active class to clicked tab
            tab.classList.add('active');

            // Hide all tab contents
            tabContents.forEach(content => {
                content.style.display = 'none';
                content.classList.remove('active');
            });

            // Show target content
            const targetId = tab.dataset.target;
            const targetContent = document.getElementById(targetId);
            if (targetContent) {
                targetContent.style.display = 'block';
                targetContent.classList.add('active');
            }

            // Hide result section on tab switch to avoid confusion
            if (resultSection) {
                resultSection.style.display = 'none';
            }
        });
    });

    // ── Calculation 1: Duration ──
    const calculateDurationBtn = document.getElementById('calculate-btn');
    const includeEndDate = document.getElementById('include-end-date');

    const resultMain = document.getElementById('result-main');
    const resultDetails = document.getElementById('result-details');
    const resultAltUnits = document.getElementById('result-alt-units');

    if (calculateDurationBtn) {
        calculateDurationBtn.addEventListener('click', () => {
            const start = getDateFromInputs('start');
            const end = getDateFromInputs('end');

            if (!isValidDate(start.d, start.m, start.y) || !isValidDate(end.d, end.m, end.y)) {
                alert('Please enter valid dates.');
                return;
            }

            const startDate = new Date(start.y, start.m - 1, start.d);
            const endDate = new Date(end.y, end.m - 1, end.d);

            let diffTime = endDate - startDate;

            if (includeEndDate.checked) {
                if (diffTime >= 0) {
                    diffTime += (24 * 60 * 60 * 1000);
                } else {
                    diffTime = Math.abs(diffTime) + (24 * 60 * 60 * 1000);
                }
            } else {
                diffTime = Math.abs(diffTime);
            }

            const totalDays = Math.round(diffTime / (1000 * 60 * 60 * 24));

            // Calendar breakdown
            let d1 = new Date(Math.min(startDate, endDate));
            let d2 = new Date(Math.max(startDate, endDate));

            if (includeEndDate.checked) {
                d2.setDate(d2.getDate() + 1);
            }

            let yDiff = d2.getFullYear() - d1.getFullYear();
            let mDiff = d2.getMonth() - d1.getMonth();
            let dDiff = d2.getDate() - d1.getDate();

            if (dDiff < 0) {
                mDiff--;
                const copy = new Date(d2.getFullYear(), d2.getMonth(), 0);
                dDiff += copy.getDate();
            }
            if (mDiff < 0) {
                yDiff--;
                mDiff += 12;
            }

            if (resultSection) resultSection.style.display = 'block';

            // Update Card Title
            document.querySelector('.result-label').textContent = 'Time Duration';

            resultMain.textContent = `${totalDays.toLocaleString()} Days`;

            const parts = [];
            if (yDiff > 0) parts.push(`${yDiff} years`);
            if (mDiff > 0) parts.push(`${mDiff} months`);
            if (dDiff > 0) parts.push(`${dDiff} days`);

            if (parts.length === 0) {
                resultDetails.textContent = 'Same day';
            } else {
                resultDetails.textContent = parts.join(', ');
            }

            // Alt units
            const weeks = Math.floor(totalDays / 7);
            const remDays = totalDays % 7;

            let altHtml = '';
            const addCard = (val, label) => {
                altHtml += `
                    <div class="alt-unit-card">
                        <div class="alt-unit-val">${val}</div>
                        <div class="alt-unit-label">${label}</div>
                    </div>
                `;
            };

            addCard((totalDays * 24 * 60 * 60).toLocaleString(), 'Seconds');
            addCard((totalDays * 24 * 60).toLocaleString(), 'Minutes');
            addCard((totalDays * 24).toLocaleString(), 'Hours');

            if (weeks > 0) {
                let weekStr = `${weeks} weeks`;
                if (remDays > 0) weekStr += ` + ${remDays} days`;
                addCard(weekStr, 'Weeks');
            } else {
                addCard('0 weeks', 'Weeks');
            }

            const yearsDec = totalDays / 365.2425;
            if (yearsDec >= 1) {
                addCard(yearsDec.toFixed(2), 'Total Years');
            } else {
                addCard(`${(yearsDec * 100).toFixed(2)}%`, 'Of a Year');
            }

            resultAltUnits.innerHTML = altHtml;
        });
    }

    // ── Calculation 2: Date +/- Days ──
    const calculateAddSubBtn = document.getElementById('calculate-addsub-btn');
    if (calculateAddSubBtn) {
        calculateAddSubBtn.addEventListener('click', () => {
            const start = getDateFromInputs('addsub');
            if (!isValidDate(start.d, start.m, start.y)) {
                alert('Please enter a valid start date.');
                return;
            }

            const startDate = new Date(start.y, start.m - 1, start.d);

            const yOps = parseInt(document.getElementById('ops-years').value || 0, 10);
            const mOps = parseInt(document.getElementById('ops-months').value || 0, 10);
            const wOps = parseInt(document.getElementById('ops-weeks').value || 0, 10);
            const dOps = parseInt(document.getElementById('ops-days').value || 0, 10);

            const op = document.querySelector('input[name="addsub-op"]:checked').value; // 'add' or 'subtract'
            const factor = op === 'subtract' ? -1 : 1;

            // Perform calculation
            // Strategy: Add years, then months, then days (weeks*7 + days)
            const resultDate = new Date(startDate);

            resultDate.setFullYear(resultDate.getFullYear() + (yOps * factor));
            resultDate.setMonth(resultDate.getMonth() + (mOps * factor));
            resultDate.setDate(resultDate.getDate() + ((wOps * 7 + dOps) * factor));

            // Display
            if (resultSection) resultSection.style.display = 'block';

            // Update Card Title
            document.querySelector('.result-label').textContent = 'Result Date';

            const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
            resultMain.textContent = resultDate.toLocaleDateString('en-US', options);
            resultDetails.textContent = op === 'add' ? 'Added duration to start date' : 'Subtracted duration from start date';
            resultAltUnits.innerHTML = ''; // Clear alt units for this mode
        });
    }


    // ── Calculation 3: Business Days ──
    const calculateBusinessBtn = document.getElementById('calculate-business-btn');
    const busIncludeEnd = document.getElementById('bus-include-end');

    if (calculateBusinessBtn) {
        calculateBusinessBtn.addEventListener('click', () => {
            const start = getDateFromInputs('bus-start');
            const end = getDateFromInputs('bus-end');

            if (!isValidDate(start.d, start.m, start.y) || !isValidDate(end.d, end.m, end.y)) {
                alert('Please enter valid dates.');
                return;
            }

            const startDate = new Date(start.y, start.m - 1, start.d);
            const endDate = new Date(end.y, end.m - 1, end.d);

            if (startDate > endDate) {
                // Swap if start > end for calculation, or handle negative?
                // Standard biz day calcs usually expect start <= end
                // Let's just swap for count and note it
            }

            let count = 0;
            let curDate = new Date(Math.min(startDate, endDate));
            const stopDate = new Date(Math.max(startDate, endDate));

            // Loop day by day
            while (curDate < stopDate) {
                const dayOfWeek = curDate.getDay();
                if (dayOfWeek !== 0 && dayOfWeek !== 6) { // 0=Sun, 6=Sat
                    count++;
                }
                curDate.setDate(curDate.getDate() + 1);
            }

            // Check end date inclusion
            if (busIncludeEnd.checked) {
                const dayOfWeek = stopDate.getDay();
                if (dayOfWeek !== 0 && dayOfWeek !== 6) {
                    count++;
                }
            }

            // Display
            if (resultSection) resultSection.style.display = 'block';

            // Update Card Title
            document.querySelector('.result-label').textContent = 'Business Days';

            resultMain.textContent = `${count} Workdays`;

            // Calculate weeks/work weeks
            const weeks = (count / 5).toFixed(1);
            resultDetails.textContent = `Does not include weekends (Sat/Sun)`;

            // Alt unit: maybe show hours (8h workday?)
            let altHtml = '';
            altHtml += `
                <div class="alt-unit-card">
                    <div class="alt-unit-val">${(count * 8).toLocaleString()}</div>
                    <div class="alt-unit-label">Work Hours (8h/day)</div>
                </div>
            `;
            altHtml += `
                <div class="alt-unit-card">
                    <div class="alt-unit-val">${weeks}</div>
                    <div class="alt-unit-label">Work Weeks</div>
                </div>
            `;

            resultAltUnits.innerHTML = altHtml;

        });
    }


    // ── Initialization ──
    setupDateListeners('start');
    setupDateListeners('end');
    setupDateListeners('addsub'); // Date +/- Days
    setupDateListeners('bus-start'); // Business days start
    setupDateListeners('bus-end'); // Business days end

    setToday('start');
    setToday('end');
    setToday('addsub');
    setToday('bus-start');
    setToday('bus-end');

})();

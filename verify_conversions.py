"""
verify_conversions.py
Comprehensive verification of ALL unit conversion combinations
Mirrors the exact logic in js/converters.js
"""

import math

# ── Conversion Data (mirrors converters.js exactly) ──────────────────────────

CONVERTERS = {
    "length": {
        "units": [
            ("meter",       "Meter (m)",              1),
            ("kilometer",   "Kilometer (km)",          1000),
            ("centimeter",  "Centimeter (cm)",         0.01),
            ("millimeter",  "Millimeter (mm)",         0.001),
            ("micrometer",  "Micrometer (µm)",         1e-6),
            ("nanometer",   "Nanometer (nm)",          1e-9),
            ("mile",        "Mile (mi)",               1609.344),
            ("yard",        "Yard (yd)",               0.9144),
            ("foot",        "Foot (ft)",               0.3048),
            ("inch",        "Inch (in)",               0.0254),
            ("nautical",    "Nautical Mile (nmi)",     1852),
            ("lightyear",   "Light Year (ly)",         9.461e15),
            ("furlong",     "Furlong",                 201.168),
            ("chain",       "Chain",                   20.1168),
        ],
        "type": "factor"
    },
    "area": {
        "units": [
            ("sqmeter",      "Square Meter (m²)",       1),
            ("sqkilometer",  "Square Kilometer (km²)",  1e6),
            ("sqcentimeter", "Square Centimeter (cm²)", 1e-4),
            ("sqmillimeter", "Square Millimeter (mm²)", 1e-6),
            ("sqmicrometer", "Square Micrometer (µm²)", 1e-12),
            ("hectare",      "Hectare (ha)",            10000),
            ("sqmile",       "Square Mile (mi²)",       2589988.11),
            ("sqyard",       "Square Yard (yd²)",       0.836127),
            ("sqfoot",       "Square Foot (ft²)",       0.092903),
            ("sqinch",       "Square Inch (in²)",       0.00064516),
            ("acre",         "Acre",                    4046.856),
        ],
        "type": "factor"
    },
    "volume": {
        "units": [
            ("liter",       "Liter (L)",               1),
            ("milliliter",  "Milliliter (mL)",          0.001),
            ("cubicmeter",  "Cubic Meter (m³)",         1000),
            ("cubicfoot",   "Cubic Foot (ft³)",         28.3168),
            ("cubicinch",   "Cubic Inch (in³)",         0.0163871),
            ("cubicyard",   "Cubic Yard (yd³)",         764.555),
            ("usgallon",    "US Gallon (gal)",          3.78541),
            ("ukgallon",    "UK Gallon (gal)",          4.54609),
            ("usquart",     "US Quart (qt)",            0.946353),
            ("uspint",      "US Pint (pt)",             0.473176),
            ("uscup",       "US Cup",                   0.236588),
            ("usfloz",      "US Fluid Ounce (fl oz)",   0.0295735),
            ("tablespoon",  "Tablespoon (tbsp)",        0.0147868),
            ("teaspoon",    "Teaspoon (tsp)",           0.00492892),
        ],
        "type": "factor"
    },
    "weight": {
        "units": [
            ("kilogram",    "Kilogram (kg)",            1),
            ("gram",        "Gram (g)",                 0.001),
            ("milligram",   "Milligram (mg)",           1e-6),
            ("microgram",   "Microgram (µg)",           1e-9),
            ("tonne",       "Metric Ton (t)",           1000),
            ("pound",       "Pound (lb)",               0.453592),
            ("ounce",       "Ounce (oz)",               0.0283495),
            ("stone",       "Stone (st)",               6.35029),
            ("uston",       "US Ton (short ton)",       907.185),
            ("ukton",       "UK Ton (long ton)",        1016.05),
            ("carat",       "Carat (ct)",               0.0002),
        ],
        "type": "factor"
    },
    "time": {
        "units": [
            ("second",      "Second (s)",               1),
            ("millisecond", "Millisecond (ms)",          0.001),
            ("microsecond", "Microsecond (µs)",          1e-6),
            ("nanosecond",  "Nanosecond (ns)",           1e-9),
            ("minute",      "Minute (min)",              60),
            ("hour",        "Hour (h)",                  3600),
            ("day",         "Day (d)",                   86400),
            ("week",        "Week (wk)",                 604800),
            ("month",       "Month (avg)",               2629800),
            ("year",        "Year (yr)",                 31557600),
            ("decade",      "Decade",                    315576000),
            ("century",     "Century",                   3155760000),
        ],
        "type": "factor"
    },
    "speed": {
        "units": [
            ("mps",         "Meter/Second (m/s)",       1),
            ("kph",         "Kilometer/Hour (km/h)",    0.277778),
            ("mph",         "Mile/Hour (mph)",          0.44704),
            ("fps",         "Foot/Second (ft/s)",       0.3048),
            ("knot",        "Knot (kn)",                0.514444),
            ("mach",        "Mach (at sea level)",      340.29),
            ("lightspeed",  "Speed of Light (c)",       299792458),
        ],
        "type": "factor"
    },
    "pressure": {
        "units": [
            ("pascal",      "Pascal (Pa)",              1),
            ("kilopascal",  "Kilopascal (kPa)",         1000),
            ("megapascal",  "Megapascal (MPa)",         1e6),
            ("bar",         "Bar",                      100000),
            ("millibar",    "Millibar (mbar)",          100),
            ("atm",         "Atmosphere (atm)",         101325),
            ("psi",         "PSI (lb/in²)",             6894.76),
            ("torr",        "Torr (mmHg)",              133.322),
            ("mmhg",        "Millimeter of Mercury",    133.322),
            ("inhg",        "Inch of Mercury (inHg)",   3386.39),
        ],
        "type": "factor"
    },
    "energy": {
        "units": [
            ("joule",       "Joule (J)",                1),
            ("kilojoule",   "Kilojoule (kJ)",           1000),
            ("megajoule",   "Megajoule (MJ)",           1e6),
            ("calorie",     "Calorie (cal)",            4.184),
            ("kilocalorie", "Kilocalorie (kcal)",        4184),
            ("wh",          "Watt-Hour (Wh)",           3600),
            ("kwh",         "Kilowatt-Hour (kWh)",      3600000),
            ("mwh",         "Megawatt-Hour (MWh)",      3.6e9),
            ("btu",         "BTU (British Thermal)",    1055.06),
            ("therm",       "Therm (US)",               1.055e8),
            ("ev",          "Electronvolt (eV)",        1.602e-19),
            ("ftlb",        "Foot-Pound (ft·lb)",       1.35582),
        ],
        "type": "factor"
    },
}

TEMPERATURE = {
    "units": [
        ("celsius",    "Celsius (°C)"),
        ("fahrenheit", "Fahrenheit (°F)"),
        ("kelvin",     "Kelvin (K)"),
        ("rankine",    "Rankine (°R)"),
        ("reaumur",    "Réaumur (°Ré)"),
    ]
}

# ── Known reference values for spot-check ────────────────────────────────────
KNOWN_VALUES = [
    # (category, from_unit, to_unit, input, expected, tolerance_pct)
    # Length
    ("length",  "meter",       "foot",        1,     3.28084,      0.01),
    ("length",  "kilometer",   "mile",        1,     0.621371,     0.01),
    ("length",  "inch",        "centimeter",  1,     2.54,         0.001),
    ("length",  "mile",        "kilometer",   1,     1.60934,      0.01),
    ("length",  "foot",        "meter",       1,     0.3048,       0.001),
    ("length",  "yard",        "meter",       1,     0.9144,       0.001),
    ("length",  "nautical",    "kilometer",   1,     1.852,        0.001),
    ("length",  "meter",       "inch",        1,     39.3701,      0.01),
    # Area
    ("area",    "sqmeter",     "sqfoot",      1,     10.7639,      0.01),
    ("area",    "acre",        "hectare",     1,     0.404686,     0.01),
    ("area",    "sqmile",      "sqkilometer", 1,     2.58999,      0.01),
    ("area",    "hectare",     "acre",        1,     2.47105,      0.01),
    ("area",    "sqfoot",      "sqmeter",     1,     0.092903,     0.001),
    # Volume
    ("volume",  "liter",       "usgallon",    1,     0.264172,     0.01),
    ("volume",  "usgallon",    "liter",       1,     3.78541,      0.001),
    ("volume",  "cubicmeter",  "liter",       1,     1000,         0.001),
    ("volume",  "liter",       "milliliter",  1,     1000,         0.001),
    ("volume",  "usfloz",      "milliliter",  1,     29.5735,      0.01),
    ("volume",  "uscup",       "milliliter",  1,     236.588,      0.01),
    # Weight
    ("weight",  "kilogram",    "pound",       1,     2.20462,      0.01),
    ("weight",  "pound",       "kilogram",    1,     0.453592,     0.001),
    ("weight",  "kilogram",    "gram",        1,     1000,         0.001),
    ("weight",  "ounce",       "gram",        1,     28.3495,      0.01),
    ("weight",  "stone",       "kilogram",    1,     6.35029,      0.001),
    ("weight",  "tonne",       "kilogram",    1,     1000,         0.001),
    # Time
    ("time",    "hour",        "minute",      1,     60,           0.001),
    ("time",    "day",         "hour",        1,     24,           0.001),
    ("time",    "year",        "day",         1,     365.25,       0.1),
    ("time",    "week",        "day",         1,     7,            0.001),
    ("time",    "minute",      "second",      1,     60,           0.001),
    # Speed
    ("speed",   "kph",         "mph",         1,     0.621371,     0.01),
    ("speed",   "mph",         "kph",         1,     1.60934,      0.01),
    ("speed",   "mps",         "kph",         1,     3.6,          0.01),
    ("speed",   "knot",        "kph",         1,     1.852,        0.01),
    # Pressure
    ("pressure","atm",         "pascal",      1,     101325,       0.01),
    ("pressure","bar",         "psi",         1,     14.5038,      0.01),
    ("pressure","psi",         "pascal",      1,     6894.76,      0.01),
    ("pressure","atm",         "psi",         1,     14.6959,      0.01),
    # Energy
    ("energy",  "joule",       "calorie",     1,     0.239006,     0.01),
    ("energy",  "kwh",         "joule",       1,     3600000,      0.001),
    ("energy",  "calorie",     "joule",       1,     4.184,        0.001),
    ("energy",  "btu",         "joule",       1,     1055.06,      0.001),
]

TEMP_KNOWN = [
    # (from, to, input, expected, tol)
    ("celsius",    "fahrenheit", 0,    32,       0.001),
    ("celsius",    "fahrenheit", 100,  212,      0.001),
    ("celsius",    "kelvin",     0,    273.15,   0.001),
    ("celsius",    "kelvin",     100,  373.15,   0.001),
    ("fahrenheit", "celsius",    32,   0,        0.001),
    ("fahrenheit", "celsius",    212,  100,      0.001),
    ("fahrenheit", "celsius",    98.6, 37,       0.01),
    ("kelvin",     "celsius",    273.15, 0,      0.001),
    ("kelvin",     "fahrenheit", 373.15, 212,    0.001),
    ("celsius",    "rankine",    0,    491.67,   0.01),
    ("celsius",    "reaumur",    100,  80,       0.001),
    ("reaumur",    "celsius",    80,   100,      0.001),
]

# ── Conversion functions ──────────────────────────────────────────────────────

def factor_convert(value, from_id, to_id, units):
    factors = {uid: f for uid, _, f in units}
    return value * factors[from_id] / factors[to_id]

def temp_convert(value, from_id, to_id):
    # to celsius
    if from_id == "celsius":    c = value
    elif from_id == "fahrenheit": c = (value - 32) * 5/9
    elif from_id == "kelvin":   c = value - 273.15
    elif from_id == "rankine":  c = (value - 491.67) * 5/9
    elif from_id == "reaumur":  c = value * 5/4
    else: return float('nan')
    # from celsius
    if to_id == "celsius":      return c
    elif to_id == "fahrenheit": return c * 9/5 + 32
    elif to_id == "kelvin":     return c + 273.15
    elif to_id == "rankine":    return (c + 273.15) * 9/5
    elif to_id == "reaumur":    return c * 4/5
    else: return float('nan')

# ── Run all combinations ──────────────────────────────────────────────────────

PASS = 0
FAIL = 0
ERRORS = []
RESULTS = []

TEST_VALUES = [1, 10, 100, 0.5, 1000]

print("=" * 80)
print("UNIT CONVERTER — FULL COMBINATION VERIFICATION")
print("=" * 80)

# Factor-based categories
for cat_name, cat_data in CONVERTERS.items():
    units = cat_data["units"]
    unit_ids = [u[0] for u in units]
    unit_labels = {u[0]: u[1] for u in units}
    combos = 0
    cat_pass = 0
    cat_fail = 0

    for from_id in unit_ids:
        for to_id in unit_ids:
            if from_id == to_id:
                # Self-conversion: must equal input
                for val in TEST_VALUES:
                    result = factor_convert(val, from_id, to_id, units)
                    ok = abs(result - val) < 1e-9
                    if ok:
                        cat_pass += 1
                    else:
                        cat_fail += 1
                        ERRORS.append(f"[{cat_name}] {from_id}→{to_id} val={val}: got {result}, expected {val}")
                    combos += 1
            else:
                for val in TEST_VALUES:
                    result = factor_convert(val, from_id, to_id, units)
                    # Verify round-trip
                    roundtrip = factor_convert(result, to_id, from_id, units)
                    ok = abs(roundtrip - val) / max(abs(val), 1e-15) < 1e-8
                    if ok:
                        cat_pass += 1
                    else:
                        cat_fail += 1
                        ERRORS.append(f"[{cat_name}] ROUNDTRIP {from_id}→{to_id}→{from_id} val={val}: got {roundtrip}, expected {val}")
                    combos += 1

    PASS += cat_pass
    FAIL += cat_fail
    n_units = len(units)
    print(f"\n  [{cat_name.upper():12s}] {n_units} units | {combos} combinations | PASS={cat_pass} FAIL={cat_fail}")

# Temperature
print(f"\n  [TEMPERATURE ] 5 units | all combinations |", end=" ")
temp_units = [u[0] for u in TEMPERATURE["units"]]
t_pass = 0
t_fail = 0
for from_id in temp_units:
    for to_id in temp_units:
        for val in [-40, 0, 20, 37, 100, 200]:
            result = temp_convert(val, from_id, to_id)
            if from_id == to_id:
                ok = abs(result - val) < 1e-9
            else:
                roundtrip = temp_convert(result, to_id, from_id)
                ok = abs(roundtrip - val) < 1e-6
            if ok:
                t_pass += 1
            else:
                t_fail += 1
                ERRORS.append(f"[temperature] ROUNDTRIP {from_id}→{to_id}→{from_id} val={val}: got {roundtrip:.6f}, expected {val}")
PASS += t_pass
FAIL += t_fail
print(f"PASS={t_pass} FAIL={t_fail}")

# ── Known reference spot-checks ───────────────────────────────────────────────
print("\n" + "=" * 80)
print("KNOWN REFERENCE VALUE SPOT-CHECKS")
print("=" * 80)

spot_pass = 0
spot_fail = 0

for cat, from_id, to_id, inp, expected, tol_pct in KNOWN_VALUES:
    units = CONVERTERS[cat]["units"]
    result = factor_convert(inp, from_id, to_id, units)
    err_pct = abs(result - expected) / abs(expected) * 100 if expected != 0 else abs(result)
    ok = err_pct <= tol_pct
    status = "PASS" if ok else "FAIL"
    if ok:
        spot_pass += 1
    else:
        spot_fail += 1
        ERRORS.append(f"SPOT [{cat}] {inp} {from_id}→{to_id}: got {result:.6g}, expected {expected:.6g} (err={err_pct:.4f}%)")
    got_str = f"{result:.6g}"
    print(f"  [{status}] {cat:10s} | {inp} {from_id:15s} -> {to_id:15s} | got {got_str:>18} | expected {expected:.6g}")

print(f"\n  Temperature spot-checks:")
for from_id, to_id, inp, expected, tol in TEMP_KNOWN:
    result = temp_convert(inp, from_id, to_id)
    err = abs(result - expected)
    ok = err <= tol
    status = "PASS" if ok else "FAIL"
    if ok:
        spot_pass += 1
    else:
        spot_fail += 1
        ERRORS.append(f"SPOT [temp] {inp} {from_id}→{to_id}: got {result:.6f}, expected {expected:.6f}")
    got_str2 = f"{result:.4f}"
    print(f"  [{status}] temperature | {inp} {from_id:15s} -> {to_id:15s} | got {got_str2:>12} | expected {expected:.4f}")

# ── Summary ───────────────────────────────────────────────────────────────────
total = PASS + FAIL + spot_pass + spot_fail
print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"  Round-trip tests : {PASS + FAIL:>6}  |  PASS: {PASS}  |  FAIL: {FAIL}")
print(f"  Spot-check tests : {spot_pass + spot_fail:>6}  |  PASS: {spot_pass}  |  FAIL: {spot_fail}")
print(f"  TOTAL            : {total:>6}  |  PASS: {PASS+spot_pass}  |  FAIL: {FAIL+spot_fail}")

if ERRORS:
    print("\n  FAILURES:")
    for e in ERRORS:
        print(f"    ✗ {e}")
else:
    print("\n  ALL TESTS PASSED ✓")
print("=" * 80)

"""
gen_pair_pages.py
Generates individual conversion pair pages for every unit pair in every category.
URL structure: /{category}/{from-slug}-to-{to-slug}/index.html
"""

import os, math, itertools

BASE = r"C:\Users\Administrator\Documents\AntiGravity\Units"
if os.name == 'posix':
    BASE = os.getcwd()

ADSENSE_PUB_ID = "ca-pub-2662293899276634"

# ── Unit data (mirrors converters.js exactly) ─────────────────────────────────
CATEGORIES = {
    "length": {
        "name": "Length", "cat_label": "Length Conversion",
        "units": [
            ("meter",       "Meter",              "m",      1),
            ("kilometer",   "Kilometer",          "km",     1000),
            ("centimeter",  "Centimeter",         "cm",     0.01),
            ("millimeter",  "Millimeter",         "mm",     0.001),
            ("micrometer",  "Micrometer",         "µm",     1e-6),
            ("nanometer",   "Nanometer",          "nm",     1e-9),
            ("mile",        "Mile",               "mi",     1609.344),
            ("yard",        "Yard",               "yd",     0.9144),
            ("foot",        "Foot",               "ft",     0.3048),
            ("inch",        "Inch",               "in",     0.0254),
            ("nautical",    "Nautical Mile",      "nmi",    1852),
            ("lightyear",   "Light Year",         "ly",     9.461e15),
            ("furlong",     "Furlong",            "fur",    201.168),
            ("chain",       "Chain",              "ch",     20.1168),
        ],
        "definitions": {
            "meter":      "The meter is the base unit of length in the International System of Units (SI). It is defined as the distance light travels in vacuum in 1/299,792,458 of a second.",
            "kilometer":  "A kilometer equals 1,000 meters. It is commonly used to measure distances between geographical locations.",
            "centimeter": "A centimeter is one hundredth of a meter. It is widely used in everyday measurements such as height and clothing sizes.",
            "millimeter": "A millimeter is one thousandth of a meter. It is used for precise measurements in engineering and manufacturing.",
            "micrometer": "A micrometer (micron) is one millionth of a meter. It is used in science and engineering for very small measurements.",
            "nanometer":  "A nanometer is one billionth of a meter. It is used in nanotechnology and to describe wavelengths of light.",
            "mile":       "A mile is a unit of length equal to 5,280 feet or 1,760 yards. It is used in the United States and United Kingdom.",
            "yard":       "A yard equals 3 feet or 36 inches. It is used in the United States and United Kingdom for measuring fabric and sports fields.",
            "foot":       "A foot equals 12 inches. It is used in the United States and United Kingdom for height and short distances.",
            "inch":       "An inch is 1/12 of a foot. It is used in the United States and United Kingdom for small measurements.",
            "nautical":   "A nautical mile equals 1,852 meters. It is used in maritime and aviation navigation.",
            "lightyear":  "A light year is the distance light travels in one year, approximately 9.461 × 10¹⁵ meters.",
            "furlong":    "A furlong equals 201.168 meters or 1/8 of a mile. It is used in horse racing.",
            "chain":      "A chain equals 20.1168 meters. It is a unit of length used in surveying.",
        }
    },
    "temperature": {
        "name": "Temperature", "cat_label": "Temperature Conversion",
        "units": [
            ("celsius",    "Celsius",    "°C",  None),
            ("fahrenheit", "Fahrenheit", "°F",  None),
            ("kelvin",     "Kelvin",     "K",   None),
            ("rankine",    "Rankine",    "°R",  None),
            ("reaumur",    "Reaumur",    "°Re", None),
        ],
        "definitions": {
            "celsius":    "Celsius (°C) is a temperature scale where 0°C is the freezing point of water and 100°C is the boiling point at standard pressure.",
            "fahrenheit": "Fahrenheit (°F) is a temperature scale where 32°F is the freezing point of water and 212°F is the boiling point. Used mainly in the United States.",
            "kelvin":     "Kelvin (K) is the SI base unit of temperature. 0 K is absolute zero, the lowest possible temperature.",
            "rankine":    "Rankine (°R) is an absolute temperature scale based on Fahrenheit degrees. 0 °R is absolute zero.",
            "reaumur":    "Réaumur (°Re) is a temperature scale where 0°Re is the freezing point and 80°Re is the boiling point of water.",
        }
    },
    "area": {
        "name": "Area", "cat_label": "Area Conversion",
        "units": [
            ("sqmeter",      "Square Meter",      "m²",   1),
            ("sqkilometer",  "Square Kilometer",  "km²",  1e6),
            ("sqcentimeter", "Square Centimeter", "cm²",  1e-4),
            ("sqmillimeter", "Square Millimeter", "mm²",  1e-6),
            ("sqmicrometer", "Square Micrometer", "µm²",  1e-12),
            ("hectare",      "Hectare",           "ha",   10000),
            ("sqmile",       "Square Mile",       "mi²",  2589988.11),
            ("sqyard",       "Square Yard",       "yd²",  0.836127),
            ("sqfoot",       "Square Foot",       "ft²",  0.092903),
            ("sqinch",       "Square Inch",       "in²",  0.00064516),
            ("acre",         "Acre",              "ac",   4046.856),
        ],
        "definitions": {
            "sqmeter":      "A square meter is the SI unit of area, equal to the area of a square with sides of one meter.",
            "sqkilometer":  "A square kilometer equals 1,000,000 square meters. Used for measuring large land areas.",
            "sqcentimeter": "A square centimeter equals 0.0001 square meters. Used for small area measurements.",
            "sqmillimeter": "A square millimeter equals 0.000001 square meters. Used in engineering and science.",
            "sqmicrometer": "A square micrometer equals 10⁻¹² square meters. Used in microscopy and nanotechnology.",
            "hectare":      "A hectare equals 10,000 square meters. It is the primary unit for measuring land area in agriculture.",
            "sqmile":       "A square mile equals 2,589,988 square meters. Used in the United States for large land areas.",
            "sqyard":       "A square yard equals 0.836127 square meters. Used in the United States and United Kingdom.",
            "sqfoot":       "A square foot equals 0.092903 square meters. Widely used in real estate in the United States.",
            "sqinch":       "A square inch equals 0.00064516 square meters. Used for small area measurements.",
            "acre":         "An acre equals 4,046.856 square meters. It is used in the United States and United Kingdom for land measurement.",
        }
    },
    "volume": {
        "name": "Volume", "cat_label": "Volume Conversion",
        "units": [
            ("liter",       "Liter",             "L",      1),
            ("milliliter",  "Milliliter",         "mL",     0.001),
            ("cubicmeter",  "Cubic Meter",        "m³",     1000),
            ("cubicfoot",   "Cubic Foot",         "ft³",    28.3168),
            ("cubicinch",   "Cubic Inch",         "in³",    0.0163871),
            ("cubicyard",   "Cubic Yard",         "yd³",    764.555),
            ("usgallon",    "US Gallon",          "gal",    3.78541),
            ("ukgallon",    "UK Gallon",          "gal",    4.54609),
            ("usquart",     "US Quart",           "qt",     0.946353),
            ("uspint",      "US Pint",            "pt",     0.473176),
            ("uscup",       "US Cup",             "cup",    0.236588),
            ("usfloz",      "US Fluid Ounce",     "fl oz",  0.0295735),
            ("tablespoon",  "Tablespoon",         "tbsp",   0.0147868),
            ("teaspoon",    "Teaspoon",           "tsp",    0.00492892),
        ],
        "definitions": {
            "liter":       "A liter is a metric unit of volume equal to 1,000 milliliters or 1 cubic decimeter. Widely used for liquids.",
            "milliliter":  "A milliliter is one thousandth of a liter. Used for small liquid measurements in cooking and medicine.",
            "cubicmeter":  "A cubic meter is the SI unit of volume, equal to 1,000 liters. Used for large volumes.",
            "cubicfoot":   "A cubic foot equals 28.3168 liters. Used in the United States for volume of rooms and containers.",
            "cubicinch":   "A cubic inch equals 0.0163871 liters. Used in the United States for engine displacement.",
            "cubicyard":   "A cubic yard equals 764.555 liters. Used in the United States for concrete and soil.",
            "usgallon":    "A US gallon equals 3.78541 liters. It is the standard gallon used in the United States.",
            "ukgallon":    "A UK (imperial) gallon equals 4.54609 liters. Used in the United Kingdom and Canada.",
            "usquart":     "A US quart equals 0.946353 liters or one quarter of a US gallon.",
            "uspint":      "A US pint equals 0.473176 liters or one half of a US quart.",
            "uscup":       "A US cup equals 0.236588 liters or 8 US fluid ounces. Used in cooking.",
            "usfloz":      "A US fluid ounce equals 0.0295735 liters. Used for small liquid measurements.",
            "tablespoon":  "A tablespoon equals 0.0147868 liters or 3 teaspoons. Used in cooking.",
            "teaspoon":    "A teaspoon equals 0.00492892 liters. The smallest common cooking measurement.",
        }
    },
    "weight": {
        "name": "Weight", "cat_label": "Weight and Mass Conversion",
        "units": [
            ("kilogram",    "Kilogram",       "kg",   1),
            ("gram",        "Gram",           "g",    0.001),
            ("milligram",   "Milligram",      "mg",   1e-6),
            ("microgram",   "Microgram",      "µg",   1e-9),
            ("tonne",       "Metric Ton",     "t",    1000),
            ("pound",       "Pound",          "lb",   0.453592),
            ("ounce",       "Ounce",          "oz",   0.0283495),
            ("stone",       "Stone",          "st",   6.35029),
            ("uston",       "US Ton",         "ton",  907.185),
            ("ukton",       "UK Ton",         "LT",   1016.05),
            ("carat",       "Carat",          "ct",   0.0002),
        ],
        "definitions": {
            "kilogram":   "A kilogram is the SI base unit of mass. It is defined by the Planck constant and is equal to 1,000 grams.",
            "gram":       "A gram is one thousandth of a kilogram. Used for small mass measurements in cooking and science.",
            "milligram":  "A milligram is one thousandth of a gram. Used in medicine and pharmacology.",
            "microgram":  "A microgram is one millionth of a gram. Used in scientific and medical contexts.",
            "tonne":      "A metric ton (tonne) equals 1,000 kilograms. Used for large mass measurements in industry.",
            "pound":      "A pound equals 0.453592 kilograms. It is the primary unit of mass in the United States.",
            "ounce":      "An ounce equals 0.0283495 kilograms or 1/16 of a pound. Used in the United States for food.",
            "stone":      "A stone equals 6.35029 kilograms or 14 pounds. Used in the United Kingdom for body weight.",
            "uston":      "A US ton (short ton) equals 907.185 kilograms or 2,000 pounds.",
            "ukton":      "A UK ton (long ton) equals 1,016.05 kilograms or 2,240 pounds.",
            "carat":      "A carat equals 0.2 grams. Used for measuring the mass of gemstones.",
        }
    },
    "time": {
        "name": "Time", "cat_label": "Time Conversion",
        "units": [
            ("second",      "Second",      "s",    1),
            ("millisecond", "Millisecond", "ms",   0.001),
            ("microsecond", "Microsecond", "µs",   1e-6),
            ("nanosecond",  "Nanosecond",  "ns",   1e-9),
            ("minute",      "Minute",      "min",  60),
            ("hour",        "Hour",        "h",    3600),
            ("day",         "Day",         "d",    86400),
            ("week",        "Week",        "wk",   604800),
            ("month",       "Month",       "mo",   2629800),
            ("year",        "Year",        "yr",   31557600),
            ("decade",      "Decade",      "dec",  315576000),
            ("century",     "Century",     "c",    3155760000),
        ],
        "definitions": {
            "second":      "The second is the SI base unit of time. It is defined by the cesium-133 atomic clock.",
            "millisecond": "A millisecond is one thousandth of a second. Used in computing and sports timing.",
            "microsecond": "A microsecond is one millionth of a second. Used in electronics and physics.",
            "nanosecond":  "A nanosecond is one billionth of a second. Used in computing and telecommunications.",
            "minute":      "A minute equals 60 seconds. It is a common unit of time for everyday use.",
            "hour":        "An hour equals 3,600 seconds or 60 minutes. It is a standard unit for measuring time of day.",
            "day":         "A day equals 86,400 seconds or 24 hours. It is the time for one rotation of the Earth.",
            "week":        "A week equals 7 days or 604,800 seconds. It is a standard unit in calendars worldwide.",
            "month":       "A month averages 30.44 days or 2,629,800 seconds. It is based on the lunar cycle.",
            "year":        "A year equals 365.25 days or 31,557,600 seconds. It is the time for Earth to orbit the Sun.",
            "decade":      "A decade equals 10 years. Used for historical and generational time periods.",
            "century":     "A century equals 100 years. Used for historical time periods.",
        }
    },
    "speed": {
        "name": "Speed", "cat_label": "Speed Conversion",
        "units": [
            ("mps",        "Meter per Second",      "m/s",  1),
            ("kph",        "Kilometer per Hour",    "km/h", 0.277778),
            ("mph",        "Mile per Hour",         "mph",  0.44704),
            ("fps",        "Foot per Second",       "ft/s", 0.3048),
            ("knot",       "Knot",                  "kn",   0.514444),
            ("mach",       "Mach",                  "Ma",   340.29),
            ("lightspeed", "Speed of Light",        "c",    299792458),
        ],
        "definitions": {
            "mps":        "Meters per second (m/s) is the SI unit of speed. It measures how many meters are traveled in one second.",
            "kph":        "Kilometers per hour (km/h) is a unit of speed widely used in road transport worldwide.",
            "mph":        "Miles per hour (mph) is a unit of speed used in the United States and United Kingdom for road transport.",
            "fps":        "Feet per second (ft/s) is a unit of speed used in the United States, especially in ballistics.",
            "knot":       "A knot equals one nautical mile per hour (1.852 km/h). Used in maritime and aviation navigation.",
            "mach":       "Mach is the ratio of speed to the speed of sound. Mach 1 equals approximately 340.29 m/s at sea level.",
            "lightspeed": "The speed of light (c) is approximately 299,792,458 m/s. It is the maximum speed at which energy can travel.",
        }
    },
    "pressure": {
        "name": "Pressure", "cat_label": "Pressure Conversion",
        "units": [
            ("pascal",     "Pascal",                 "Pa",   1),
            ("kilopascal", "Kilopascal",             "kPa",  1000),
            ("megapascal", "Megapascal",             "MPa",  1e6),
            ("bar",        "Bar",                    "bar",  100000),
            ("millibar",   "Millibar",               "mbar", 100),
            ("atm",        "Atmosphere",             "atm",  101325),
            ("psi",        "PSI",                    "psi",  6894.76),
            ("torr",       "Torr",                   "Torr", 133.322),
            ("mmhg",       "Millimeter of Mercury",  "mmHg", 133.322),
            ("inhg",       "Inch of Mercury",        "inHg", 3386.39),
        ],
        "definitions": {
            "pascal":     "The pascal (Pa) is the SI unit of pressure, equal to one newton per square meter.",
            "kilopascal": "A kilopascal equals 1,000 pascals. Used for tire pressure and atmospheric measurements.",
            "megapascal": "A megapascal equals 1,000,000 pascals. Used in engineering for material strength.",
            "bar":        "A bar equals 100,000 pascals. It is close to standard atmospheric pressure (1 atm = 1.01325 bar).",
            "millibar":   "A millibar equals 100 pascals. Used in meteorology for atmospheric pressure.",
            "atm":        "An atmosphere (atm) equals 101,325 pascals. It represents standard atmospheric pressure at sea level.",
            "psi":        "PSI (pounds per square inch) equals 6,894.76 pascals. Used in the United States for tire and fluid pressure.",
            "torr":       "A torr equals 133.322 pascals. It is defined as 1/760 of an atmosphere.",
            "mmhg":       "Millimeter of mercury (mmHg) equals 133.322 pascals. Used in medicine for blood pressure.",
            "inhg":       "Inch of mercury (inHg) equals 3,386.39 pascals. Used in aviation and meteorology.",
        }
    },
    "energy": {
        "name": "Energy", "cat_label": "Energy Conversion",
        "units": [
            ("joule",       "Joule",           "J",    1),
            ("kilojoule",   "Kilojoule",       "kJ",   1000),
            ("megajoule",   "Megajoule",       "MJ",   1e6),
            ("calorie",     "Calorie",         "cal",  4.184),
            ("kilocalorie", "Kilocalorie",     "kcal", 4184),
            ("wh",          "Watt-Hour",       "Wh",   3600),
            ("kwh",         "Kilowatt-Hour",   "kWh",  3600000),
            ("mwh",         "Megawatt-Hour",   "MWh",  3.6e9),
            ("btu",         "BTU",             "BTU",  1055.06),
            ("therm",       "Therm",           "thm",  1.055e8),
            ("ev",          "Electronvolt",    "eV",   1.602e-19),
            ("ftlb",        "Foot-Pound",      "ft·lb",1.35582),
        ],
        "definitions": {
            "joule":       "The joule (J) is the SI unit of energy, equal to the work done by a force of one newton over one meter.",
            "kilojoule":   "A kilojoule equals 1,000 joules. Used in nutrition to measure food energy.",
            "megajoule":   "A megajoule equals 1,000,000 joules. Used in engineering and physics.",
            "calorie":     "A calorie equals 4.184 joules. It is the energy needed to raise 1 gram of water by 1°C.",
            "kilocalorie": "A kilocalorie (food calorie) equals 4,184 joules. Used in nutrition for food energy content.",
            "wh":          "A watt-hour equals 3,600 joules. Used for measuring electrical energy consumption.",
            "kwh":         "A kilowatt-hour equals 3,600,000 joules. The standard unit for electricity billing.",
            "mwh":         "A megawatt-hour equals 3,600,000,000 joules. Used for large-scale power generation.",
            "btu":         "A BTU (British Thermal Unit) equals 1,055.06 joules. Used in heating and cooling systems.",
            "therm":       "A therm equals 105,480,400 joules or 100,000 BTU. Used for natural gas billing.",
            "ev":          "An electronvolt (eV) equals 1.602 × 10⁻¹⁹ joules. Used in atomic and particle physics.",
            "ftlb":        "A foot-pound equals 1.35582 joules. Used in the United States for torque and energy.",
        }
    },
}

# ── Conversion helpers ────────────────────────────────────────────────────────

def factor_convert(value, from_factor, to_factor):
    return value * from_factor / to_factor

def temp_convert(value, from_id, to_id):
    if from_id == "celsius":    c = value
    elif from_id == "fahrenheit": c = (value - 32) * 5/9
    elif from_id == "kelvin":   c = value - 273.15
    elif from_id == "rankine":  c = (value - 491.67) * 5/9
    elif from_id == "reaumur":  c = value * 5/4
    else: return float('nan')
    if to_id == "celsius":      return c
    elif to_id == "fahrenheit": return c * 9/5 + 32
    elif to_id == "kelvin":     return c + 273.15
    elif to_id == "rankine":    return (c + 273.15) * 9/5
    elif to_id == "reaumur":    return c * 4/5
    else: return float('nan')

def fmt(num):
    """Format a number as a human-readable string without exponential notation."""
    if math.isnan(num) or math.isinf(num): return "N/A"
    if num == 0: return "0"
    abs_n = abs(num)
    # Round to 10 significant digits to eliminate floating-point noise
    # e.g. 1/1e-9 = 999999999.9999999 → rounds to 1000000000
    if abs_n > 0:
        sig = 10
        magnitude = math.floor(math.log10(abs_n))
        rounded = round(num, -int(magnitude) + sig - 1)
    else:
        rounded = num
    abs_r = abs(rounded)
    # Very small numbers: show enough decimal places
    if abs_r <= 0.000001 and abs_r > 0:
        decimals = max(0, -int(math.floor(math.log10(abs_r))) + 5)
        decimals = min(decimals, 20)
        return f"{rounded:.{decimals}f}".rstrip('0').rstrip('.')
    # Large numbers: always show as full integer or decimal with commas
    if abs_r >= 1000:
        if rounded == int(rounded):
            return f"{int(rounded):,}"
        # Non-integer large number: show with enough decimal places
        decimals = max(0, sig - 1 - int(math.floor(math.log10(abs_r))))
        return f"{rounded:,.{decimals}f}".rstrip('0').rstrip('.')
    # Normal range (< 1000)
    return f"{rounded:.10g}"

def slug(name):
    return name.lower().replace(" ", "-").replace("/", "-per-").replace("(", "").replace(")", "").replace("°", "").replace("²", "2").replace("³", "3").replace("·", "-").replace("µ", "u")

# ── Build slug map ────────────────────────────────────────────────────────────
# unit_id -> url_slug (for filenames)
SLUG_MAP = {}
for cat_key, cat in CATEGORIES.items():
    for uid, uname, usym, *_ in cat["units"]:
        s = slug(uname)
        SLUG_MAP[(cat_key, uid)] = s

# ── HTML template ─────────────────────────────────────────────────────────────

def make_page(cat_key, cat, from_unit, to_unit):
    fid, fname, fsym, *frest = from_unit
    tid, tname, tsym, *trest = to_unit

    ffactor = frest[0] if frest else None
    tfactor = trest[0] if trest else None

    from_slug = SLUG_MAP[(cat_key, fid)]
    to_slug   = SLUG_MAP[(cat_key, tid)]
    page_slug = f"{from_slug}-to-{to_slug}"
    reverse_slug = f"{to_slug}-to-{from_slug}"

    cat_name = cat["name"]
    cat_label = cat["cat_label"]
    definition = cat["definitions"].get(fid, f"{fname} is a unit of {cat_name.lower()}.")

    # Conversion factor display
    is_temp = (cat_key == "temperature")
    if is_temp:
        factor_1_fwd = temp_convert(1, fid, tid)
        factor_1_rev = temp_convert(1, tid, fid)
        example_val = 20
        example_result = temp_convert(example_val, fid, tid)
        formula_fwd = f"1 {fname} ({fsym}) = {fmt(factor_1_fwd)} {tname} ({tsym})"
        formula_rev = f"1 {tname} ({tsym}) = {fmt(factor_1_rev)} {fname} ({fsym})"
        example_str = f"{example_val} {fname} ({fsym}) = {fmt(example_result)} {tname} ({tsym})"
        table_vals = [-40, 0, 20, 37, 100, 200, 500]
    else:
        factor_1_fwd = ffactor / tfactor
        factor_1_rev = tfactor / ffactor
        formula_fwd = f"1 {fname} ({fsym}) = {fmt(factor_1_fwd)} {tname} ({tsym})"
        formula_rev = f"1 {tname} ({tsym}) = {fmt(factor_1_rev)} {fname} ({fsym})"
        example_val = 15
        example_result = example_val * ffactor / tfactor
        example_str = f"{example_val} {fname} ({fsym}) = {example_val} &times; {fmt(factor_1_fwd)} {tname} ({tsym}) = {fmt(example_result)} {tname} ({tsym})"
        table_vals = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]

    # Conversion table rows
    table_rows = ""
    for v in table_vals:
        if is_temp:
            r = temp_convert(v, fid, tid)
        else:
            r = v * ffactor / tfactor
        table_rows += f"<tr><td>{v} {fsym}</td><td>{fmt(r)} {tsym}</td></tr>\n"

    # Related conversions (all other pairs in same category, up to 24)
    related_left = []
    related_right = []
    all_units = cat["units"]
    related_pairs = []
    for u1 in all_units:
        for u2 in all_units:
            if u1[0] == u2[0]: continue
            if u1[0] == fid and u2[0] == tid: continue  # skip self
            s1 = SLUG_MAP[(cat_key, u1[0])]
            s2 = SLUG_MAP[(cat_key, u2[0])]
            label = f"{u1[1]} to {u2[1]}"
            href  = f"../{s1}-to-{s2}/"
            related_pairs.append((label, href))

    # Deduplicate and limit
    seen = set()
    unique_related = []
    for label, href in related_pairs:
        if label not in seen:
            seen.add(label)
            unique_related.append((label, href))

    # Split into two columns
    half = (len(unique_related) + 1) // 2
    col1 = unique_related[:half]
    col2 = unique_related[half:]

    def make_li(label, href):
        return f'<li><a href="{href}">{label}</a></li>'

    col1_html = "\n".join(make_li(l, h) for l, h in col1)
    col2_html = "\n".join(make_li(l, h) for l, h in col2)

    # Nav links
    nav_links = ""
    nav_cats = [
        ("length","📏 Length"), ("temperature","🌡️ Temperature"), ("area","⬛ Area"),
        ("volume","🧊 Volume"), ("weight","⚖️ Weight"), ("time","⏱️ Time"),
        ("speed","🚀 Speed"), ("pressure","🔵 Pressure"), ("energy","⚡ Energy"),
        ("land","🌾 Land"),
    ]
    for nk, nn in nav_cats:
        active = ' class="nav-link active"' if nk == cat_key else ' class="nav-link"'
        nav_links += f'<a href="../../{nk}/"{active}>{nn}</a>\n      '

    # Sidebar links
    sidebar_links = ""
    for nk, nn in nav_cats:
        active = ' active' if nk == cat_key else ''
        sidebar_links += f'<a href="../../{nk}/" class="sidebar-link{active}">{nn} Converter</a>\n          '

    title = f"Convert {fname} to {tname} | {fname} to {tname} Converter"
    desc  = f"Easily convert {fname} ({fsym}) to {tname} ({tsym}). Free online {cat_name.lower()} converter with formula, examples, and conversion table."
    kw    = f"{fname} to {tname}, {fsym} to {tsym}, convert {fname} to {tname}, {cat_name.lower()} converter, {fname} {tname} conversion"
    canonical = f"https://www.unitconvert.net/{cat_key}/{page_slug}/"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content="{desc}" />
  <meta name="keywords" content="{kw}" />
  <meta name="robots" content="index, follow" />
  <link rel="canonical" href="{canonical}" />
  <meta property="og:title" content="Convert {fname} to {tname}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:type" content="website" />
  <meta name="twitter:card" content="summary" />
  <meta name="twitter:title" content="Convert {fname} to {tname}" />
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "WebApplication",
    "name": "Convert {fname} to {tname}",
    "url": "{canonical}",
    "description": "{desc}",
    "applicationCategory": "UtilitiesApplication",
    "operatingSystem": "Any",
    "offers": {{"@type": "Offer", "price": "0", "priceCurrency": "USD"}}
  }}
  </script>
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>&#x2696;</text></svg>" />
  <link rel="stylesheet" href="../../css/style.css" />
  <!-- Google AdSense -->
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_PUB_ID}" crossorigin="anonymous"></script>
</head>
<body data-category="{cat_key}">

  <header class="site-header" role="banner">
    <div class="header-inner">
      <a href="/" class="site-logo" aria-label="UnitConvert.net Home">
        Unit<span class="logo-accent">Convert</span><span class="logo-tld">.net</span>
      </a>
      <span class="header-tagline">Free Online Unit Converter</span>
    </div>
  </header>

  <div class="ad-header" aria-label="Advertisement">
    <!-- Middle Leaderboard -->
    <ins class="adsbygoogle ad-placeholder banner"
         style="display:inline-block;width:728px;height:90px"
         data-ad-client="{ADSENSE_PUB_ID}"
         data-ad-slot="1234567890"></ins>
    <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
  </div>

  <nav class="site-nav" role="navigation" aria-label="Converter categories">
    <div class="nav-inner">
      {nav_links}
    </div>
  </nav>

  <div class="page-wrapper">
    <main class="main-content" role="main">

      <nav class="breadcrumb" aria-label="Breadcrumb">
        <a href="/">Home</a> <span>&rsaquo;</span>
        <a href="../../{cat_key}/">{cat_label}</a> <span>&rsaquo;</span>
        <span>Convert {fname} to {tname}</span>
      </nav>

      <!-- Converter Card -->
      <article class="converter-card pair-page-card">
        <div class="converter-card-header">
          <h1>Convert {fname} to {tname}</h1>
        </div>
        <div class="pair-page-body">
          <p class="pair-intro">Please provide values below to convert <strong>{fname} [{fsym}]</strong> to <strong>{tname} [{tsym}]</strong>, or <a href="../{reverse_slug}/">vice versa</a>.</p>
          <div class="pair-converter-form">
            <div class="pair-row">
              <label>From:</label>
              <input type="number" id="pair-from" value="1" placeholder="Enter value" autocomplete="off" />
              <span class="pair-unit-label">{fname} ({fsym})</span>
            </div>
            <div class="pair-swap-row" style="display:flex; justify-content:center; margin: 8px 0;">
              <button class="swap-btn" id="pair-swap" title="Swap" aria-label="Swap units">⇄</button>
            </div>
            <div class="pair-row">
              <label>To:</label>
              <input type="text" id="pair-to" placeholder="Result" readonly />
              <span class="pair-unit-label">{tname} ({tsym})</span>
            </div>
            <div class="pair-btn-row">
              <button class="pair-convert-btn" id="pair-convert-btn">Convert</button>
              <button class="pair-clear-btn" id="pair-clear-btn">Clear</button>
            </div>
          </div>
        </div>
      </article>

      <!-- How to Convert -->
      <section class="pair-info-card">
        <h2>How to Convert {fname} to {tname}</h2>
        <p>{formula_fwd}</p>
        <p>{formula_rev}</p>
        <p><strong>Example:</strong> convert {example_val} {fname} ({fsym}) to {tname} ({tsym}):<br>
        {example_str}</p>
      </section>

      <!-- Definition -->
      <section class="pair-info-card">
        <h2>{fname} Definition</h2>
        <p>{definition}</p>
      </section>

      <!-- Conversion Table -->
      <section class="pair-table-card">
        <h2>{fname} to {tname} Conversion Table</h2>
        <table class="pair-table">
          <thead>
            <tr><th>{fname} [{fsym}]</th><th>{tname} [{tsym}]</th></tr>
          </thead>
          <tbody>
            {table_rows}
          </tbody>
        </table>
      </section>

      <!-- Related Conversions -->
      <section class="pair-related-card">
        <h2>Popular {cat_name} Conversions</h2>
        <div class="pair-related-grid">
          <ul class="pair-related-list">{col1_html}</ul>
          <ul class="pair-related-list">{col2_html}</ul>
        </div>
      </section>

    </main>

    <aside class="sidebar" role="complementary" aria-label="All converters">
      <div class="sidebar-card">
        <div class="sidebar-card-header">All Converters</div>
        <nav class="sidebar-links" aria-label="All converter categories">
          {sidebar_links}
        </nav>
      </div>
      <div aria-label="Advertisement">
        <!-- Sidebar Ad -->
        <ins class="adsbygoogle"
             style="display:block"
             data-ad-client="{ADSENSE_PUB_ID}"
             data-ad-slot="1122334455"
             data-ad-format="auto"></ins>
        <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
      </div>
    </aside>
  </div>

  <footer class="site-footer" role="contentinfo">
    <div class="footer-top" style="max-width:1200px;margin:0 auto;padding:40px 20px;display:grid;grid-template-columns:repeat(auto-fit, minmax(200px, 1fr));gap:40px;">
      <div class="footer-brand">
        <div class="site-logo">Unit<span class="logo-accent">Convert</span><span class="logo-tld">.net</span></div>
        <p style="color:rgba(255,255,255,0.6);margin-top:12px;font-size:0.9rem;line-height:1.6;">Free, fast, and accurate unit conversion for everyone. Supporting all major measurement systems worldwide.</p>
      </div>
      <div class="footer-col">
        <h4 style="color:var(--white);margin-bottom:20px;font-size:1rem;">Converters</h4>
        <ul style="list-style:none;padding:0;display:flex;flex-direction:column;gap:10px;">
          <li><a href="/length/" style="color:rgba(255,255,255,0.6);text-decoration:none;">Length</a></li>
          <li><a href="/temperature/" style="color:rgba(255,255,255,0.6);text-decoration:none;">Temperature</a></li>
          <li><a href="/area/" style="color:rgba(255,255,255,0.6);text-decoration:none;">Area</a></li>
          <li><a href="/volume/" style="color:rgba(255,255,255,0.6);text-decoration:none;">Volume</a></li>
          <li><a href="/weight/" style="color:rgba(255,255,255,0.6);text-decoration:none;">Weight</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4 style="color:var(--white);margin-bottom:20px;font-size:1rem;">More</h4>
        <ul style="list-style:none;padding:0;display:flex;flex-direction:column;gap:10px;">
          <li><a href="/time/" style="color:rgba(255,255,255,0.6);text-decoration:none;">Time</a></li>
          <li><a href="/speed/" style="color:rgba(255,255,255,0.6);text-decoration:none;">Speed</a></li>
          <li><a href="/pressure/" style="color:rgba(255,255,255,0.6);text-decoration:none;">Pressure</a></li>
          <li><a href="/energy/" style="color:rgba(255,255,255,0.6);text-decoration:none;">Energy</a></li>
          <li><a href="/land/" style="color:rgba(255,255,255,0.6);text-decoration:none;">Land</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4 style="color:var(--white);margin-bottom:20px;font-size:1rem;">Info</h4>
        <ul style="list-style:none;padding:0;display:flex;flex-direction:column;gap:10px;">
          <li><a href="/about.html" style="color:rgba(255,255,255,0.6);text-decoration:none;">About</a></li>
          <li><a href="/privacy.html" style="color:rgba(255,255,255,0.6);text-decoration:none;">Privacy Policy</a></li>
          <li><a href="/sitemap.xml" style="color:rgba(255,255,255,0.6);text-decoration:none;">Sitemap</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom" style="max-width:1200px;margin:0 auto;padding:20px;border-top:1px solid rgba(255,255,255,0.1);display:flex;justify-content:space-between;font-size:0.8rem;color:rgba(255,255,255,0.45);">
      <span>&copy; 2026 UnitConvert.net &mdash; All rights reserved.</span>
      <span><a href="/privacy.html" style="color:inherit;">Privacy</a> &middot; <a href="/sitemap.xml" style="color:inherit;">Sitemap</a></span>
    </div>
  </footer>

  <script>
  (function() {{
    var fromInput = document.getElementById('pair-from');
    var toInput   = document.getElementById('pair-to');
    var swapBtn   = document.getElementById('pair-swap');
    var convBtn   = document.getElementById('pair-convert-btn');
    var clearBtn  = document.getElementById('pair-clear-btn');
    var isSwapped = false;

    function doConvert() {{
      var val = parseFloat(String(fromInput.value).replace(/,/g, ''));
      if (isNaN(val)) {{ toInput.value = ''; return; }}
      var result;
      if (!isSwapped) {{
        {js_fwd_convert(fid, tid, ffactor, tfactor, is_temp)}
      }} else {{
        {js_fwd_convert(tid, fid, tfactor, ffactor, is_temp, swapped=True)}
      }}
      toInput.value = formatNum(result);
    }}

    function formatNum(n) {{
      if (isNaN(n) || !isFinite(n)) return '';
      if (n === 0) return '0';
      var abs = Math.abs(n);
      // Round to 10 significant digits to eliminate float noise
      var rounded = parseFloat(n.toPrecision(10));
      abs = Math.abs(rounded);
      // Very small numbers (<= 1e-6): show full decimal, no exponential
      if (abs <= 0.000001 && abs > 0) {{
        var decimals = Math.max(0, Math.min(20, -Math.floor(Math.log10(abs)) + 5));
        return rounded.toFixed(decimals).replace(/\.?0+$/, '');
      }}
      // All other numbers: plain string, no commas, no exponential
      // toFixed with enough decimals, then strip trailing zeros
      if (abs >= 1) {{
        // Integer or near-integer
        if (rounded === Math.round(rounded)) return Math.round(rounded).toString();
        // Has decimals
        var dec = Math.max(0, 9 - Math.floor(Math.log10(abs)));
        return parseFloat(rounded.toFixed(dec)).toString();
      }}
      // Between 0.000001 and 1
      return parseFloat(rounded.toPrecision(10)).toString();
    }}

    function parseInput(s) {{
      // Strip commas in case user pastes a formatted number
      return String(s).replace(/,/g, '');
    }}

    fromInput.addEventListener('input', doConvert);
    convBtn.addEventListener('click', doConvert);
    clearBtn.addEventListener('click', function() {{ fromInput.value = ''; toInput.value = ''; }});
    swapBtn.addEventListener('click', function() {{
      isSwapped = !isSwapped;
      var tmp = fromInput.value; fromInput.value = toInput.value; toInput.value = tmp;
      doConvert();
    }});
    doConvert();
  }})();
  </script>

</body>
</html>"""

def js_fwd_convert(fid, tid, ffactor, tfactor, is_temp, swapped=False):
    """Generate inline JS conversion snippet."""
    if is_temp:
        # Temperature: use hardcoded switch
        def to_c(uid, var="val"):
            m = {
                "celsius":    f"{var}",
                "fahrenheit": f"({var} - 32) * 5/9",
                "kelvin":     f"{var} - 273.15",
                "rankine":    f"({var} - 491.67) * 5/9",
                "reaumur":    f"{var} * 5/4",
            }
            return m.get(uid, "NaN")
        def from_c(uid, cvar="c"):
            m = {
                "celsius":    cvar,
                "fahrenheit": f"{cvar} * 9/5 + 32",
                "kelvin":     f"{cvar} + 273.15",
                "rankine":    f"({cvar} + 273.15) * 9/5",
                "reaumur":    f"{cvar} * 4/5",
            }
            return m.get(uid, "NaN")
        return f"var c = {to_c(fid)}; result = {from_c(tid)};"
    else:
        ff = ffactor if ffactor is not None else 1
        tf = tfactor if tfactor is not None else 1
        return f"result = val * {ff} / {tf};"

# ── Generate all pages ────────────────────────────────────────────────────────

total = 0
sitemap_entries = []

for cat_key, cat in CATEGORIES.items():
    units = cat["units"]
    for i, from_unit in enumerate(units):
        for j, to_unit in enumerate(units):
            if i == j:
                continue
            fid = from_unit[0]
            tid = to_unit[0]
            from_slug = SLUG_MAP[(cat_key, fid)]
            to_slug   = SLUG_MAP[(cat_key, tid)]
            page_slug = f"{from_slug}-to-{to_slug}"

            # Create directory
            page_dir = os.path.join(BASE, cat_key, page_slug)
            os.makedirs(page_dir, exist_ok=True)

            # Generate HTML
            html = make_page(cat_key, cat, from_unit, to_unit)

            # Write file
            out_path = os.path.join(page_dir, "index.html")
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(html)

            sitemap_entries.append(f"https://www.unitconvert.net/{cat_key}/{page_slug}/")
            total += 1

            if total % 100 == 0:
                print(f"  Generated {total} pages...")

print(f"\nTotal pages generated: {total}")

# ── Update sitemap.xml ────────────────────────────────────────────────────────
sitemap_path = os.path.join(BASE, "sitemap.xml")
with open(sitemap_path, "r", encoding="utf-8") as f:
    existing = f.read()

# Append new URLs before closing </urlset>
new_entries = "\n".join(
    f"""  <url>
    <loc>{url}</loc>
    <lastmod>2026-02-18</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>"""
    for url in sitemap_entries
)

updated = existing.replace("</urlset>", new_entries + "\n</urlset>")
with open(sitemap_path, "w", encoding="utf-8") as f:
    f.write(updated)

print(f"Sitemap updated with {len(sitemap_entries)} new URLs.")
print("Done!")

"""
gen_land_pages.py
Generates individual Indian state land unit converter pages.
URL structure: /land/{state-slug}/index.html
Base unit: Square Feet (sq ft)
"""

import os, math

BASE = r"C:\Users\Administrator\Documents\AntiGravity\Units"
if os.name == 'posix':
    BASE = os.getcwd()

LAND_DIR = os.path.join(BASE, "land")
ADSENSE_PUB_ID = "ca-pub-2662293899276634"

# ── State data ─────────────────────────────────────────────────────────────────
# Each unit: (id, label, symbol, sq_ft_factor, note)
# sq_ft_factor = how many sq ft is 1 of this unit

STATES = [
    {
        "slug": "uttar-pradesh",
        "name": "Uttar Pradesh (UP)",
        "short": "UP",
        "desc": "In UP, the Pucca Bigha is the standard for official records, while Kachha Bigha is used in local transactions.",
        "units": [
            ("sqft",        "Square Feet",    "sq ft",   1,        ""),
            ("sqmeter",     "Square Meter",   "sq m",    10.7639,  ""),
            ("gaj",         "Sq Yard (Gaj)",  "Gaj",     9,        "Commonly used for residential plots"),
            ("acre",        "Acre",           "Acre",    43560,    "Standard agricultural unit"),
            ("hectare",     "Hectare",        "ha",      107639,   "Used in official Govt. surveys"),
            ("bigha_pucca", "Bigha (Pucca)",  "Bigha P", 27225,    "Standard 'Settled' Bigha"),
            ("bigha_kachha","Bigha (Kachha)", "Bigha K", 9075,     "Exactly 1/3 of Pucca Bigha"),
            ("biswa_pucca", "Biswa (Pucca)",  "Biswa",   1361.25,  "1/20 of Pucca Bigha"),
        ],
    },
    {
        "slug": "punjab-haryana",
        "name": "Punjab & Haryana",
        "short": "PB/HR",
        "desc": "Punjab and Haryana share a system based on the Karam (~5.5 feet). The Killa equals one Acre.",
        "units": [
            ("sqft",    "Square Feet",  "sq ft",  1,       ""),
            ("sqmeter", "Square Meter", "sq m",   10.7639, ""),
            ("gaj",     "Sq Yard (Gaj)", "Gaj",    9,       ""),
            ("acre",    "Acre",         "Acre",   43560,   ""),
            ("hectare", "Hectare",      "ha",     107639,  ""),
            ("killa",   "Killa",        "Killa",  43560,   "Local name for 1 Acre"),
            ("kanal",   "Kanal",        "Kanal",  5445,    "1/8 of an Acre"),
            ("marla",   "Marla",        "Marla",  272.25,  "1/20 of a Kanal"),
            ("bigha_p", "Bigha (Pucca)","Bigha",  27225,   ""),
            ("bigha_k", "Bigha (Kachha)","Bigha K", 9075,  ""),
        ],
    },
    {
        "slug": "bihar-jharkhand",
        "name": "Bihar & Jharkhand",
        "short": "BR/JH",
        "desc": "Bihar and Jharkhand use the Katha and Dhur system, common in agricultural and rural land deals.",
        "units": [
            ("sqft",    "Square Feet",  "sq ft",  1,       ""),
            ("sqmeter", "Square Meter", "sq m",   10.7639, ""),
            ("gaj",     "Sq Yard (Gaj)", "Gaj",    9,       ""),
            ("acre",    "Acre",         "Acre",   43560,   ""),
            ("hectare", "Hectare",      "ha",     107639,  ""),
            ("bigha",   "Bigha",        "Bigha",  27220,   "Larger than Bengal Bigha"),
            ("katha",   "Katha",        "Katha",  1361,    "1/20 of Bigha"),
            ("dhur",    "Dhur",         "Dhur",   68.06,   "1/20 of Katha"),
        ],
    },
    {
        "slug": "west-bengal",
        "name": "West Bengal",
        "short": "WB",
        "desc": "Bengal uses specific smaller units like Chatak and Decimal, commonly used for small urban plots.",
        "units": [
            ("sqft",    "Square Feet",  "sq ft",  1,       ""),
            ("sqmeter", "Square Meter", "sq m",   10.7639, ""),
            ("gaj",     "Sq Yard (Gaj)", "Gaj",    9,       ""),
            ("acre",    "Acre",         "Acre",   43560,   ""),
            ("hectare", "Hectare",      "ha",     107639,  ""),
            ("bigha",   "Bigha",        "Bigha",  14400,   "Defined as 1600 sq yards"),
            ("katha",   "Katha",        "Katha",  720,     "1/20 of Bigha"),
            ("chatak",  "Chatak",       "Chatak", 180,     "1/4 of Katha"),
            ("decimal", "Decimal",      "Dec",    435.6,   "100 Decimals = 1 Acre"),
        ],
    },
    {
        "slug": "rajasthan",
        "name": "Rajasthan",
        "short": "RJ",
        "desc": "Rajasthan uses Vigha and differentiates between Pucca and Kachha Bigha.",
        "units": [
            ("sqft",        "Square Feet",    "sq ft",  1,       ""),
            ("sqmeter",     "Square Meter",   "sq m",   10.7639, ""),
            ("gaj",         "Sq Yard (Gaj)",  "Gaj",    9,       ""),
            ("acre",        "Acre",           "Acre",   43560,   ""),
            ("hectare",     "Hectare",        "ha",     107639,  ""),
            ("bigha_pucca", "Bigha (Pucca)",  "Bigha P",27225,   "Same as UP"),
            ("bigha_kachha","Bigha (Kachha)", "Bigha K",17424,   "Same as Gujarat Vigha"),
            ("biswa",       "Biswa",          "Biswa",  1361.25, "1/20 of Pucca Bigha"),
        ],
    },
    {
        "slug": "madhya-pradesh",
        "name": "Madhya Pradesh (MP)",
        "short": "MP",
        "desc": "MP uses a smaller Bigha compared to UP, along with Katha for subdivisions.",
        "units": [
            ("sqft",    "Square Feet",  "sq ft",  1,       ""),
            ("sqmeter", "Square Meter", "sq m",   10.7639, ""),
            ("gaj",     "Sq Yard (Gaj)", "Gaj",    9,       ""),
            ("acre",    "Acre",         "Acre",   43560,   ""),
            ("hectare", "Hectare",      "ha",     107639,  ""),
            ("bigha",   "Bigha",        "Bigha",  12000,   "Smaller than North Indian Bigha"),
            ("katha",   "Katha",        "Katha",  600,     "1/20 of Bigha"),
        ],
    },
    {
        "slug": "gujarat",
        "name": "Gujarat",
        "short": "GJ",
        "desc": "Gujarat uses Vigha (spelled differently from Bigha) and Guntha for land measurement.",
        "units": [
            ("sqft",    "Square Feet",  "sq ft",  1,       ""),
            ("sqmeter", "Square Meter", "sq m",   10.7639, ""),
            ("gaj",     "Sq Yard (Gaj)", "Gaj",    9,       ""),
            ("acre",    "Acre",         "Acre",   43560,   ""),
            ("hectare", "Hectare",      "ha",     107639,  ""),
            ("vigha",   "Vigha",        "Vigha",  17424,   "Measured as 132ft x 132ft"),
            ("guntha",  "Guntha",       "Guntha", 1089,    ""),
        ],
    },
    {
        "slug": "maharashtra",
        "name": "Maharashtra",
        "short": "MH",
        "desc": "Maharashtra primarily uses Guntha and Acre, avoiding Bigha in most official contexts.",
        "units": [
            ("sqft",    "Square Feet",  "sq ft",  1,       ""),
            ("sqmeter", "Square Meter", "sq m",   10.7639, ""),
            ("gaj",     "Sq Yard (Gaj)", "Gaj",    9,       ""),
            ("acre",    "Acre",         "Acre",   43560,   ""),
            ("hectare", "Hectare",      "ha",     107639,  ""),
            ("guntha",  "Guntha",       "Guntha", 1089,    "Widely used across the state"),
        ],
    },
    {
        "slug": "tamil-nadu",
        "name": "Tamil Nadu",
        "short": "TN",
        "desc": "Tamil Nadu uses a completely different system. Ground is the standard unit for residential plots in Chennai.",
        "units": [
            ("sqft",    "Square Feet",  "sq ft",  1,       ""),
            ("sqmeter", "Square Meter", "sq m",   10.7639, ""),
            ("gaj",     "Sq Yard (Gaj)", "Gaj",    9,       ""),
            ("acre",    "Acre",         "Acre",   43560,   ""),
            ("hectare", "Hectare",      "ha",     107639,  ""),
            ("ground",  "Ground",       "Ground", 2400,    "Standard for Chennai real estate"),
            ("cent",    "Cent",         "Cent",   435.6,   "1/100 of an Acre"),
        ],
    },
    {
        "slug": "himachal-uttarakhand-jk",
        "name": "HP, Uttarakhand & J&K",
        "short": "North Hilly",
        "desc": "Hilly terrain states like Himachal, Uttarakhand, and J&K use smaller units due to the stepped landscape.",
        "units": [
            ("sqft",    "Square Feet",  "sq ft",  1,       ""),
            ("sqmeter", "Square Meter", "sq m",   10.7639, ""),
            ("gaj",     "Sq Yard (Gaj)", "Gaj",    9,       ""),
            ("acre",    "Acre",         "Acre",   43560,   ""),
            ("hectare", "Hectare",      "ha",     107639,  ""),
            ("bigha",   "Bigha",        "Bigha",  8712,    "Smaller hilly Bigha"),
            ("biswa",   "Biswa",        "Biswa",  435.6,   "1/20 of Bigha"),
            ("nali",    "Nali",         "Nali",   2160,    "Unique to Uttarakhand"),
            ("muthi",   "Muthi",        "Muthi",  135,     "1/16 of a Nali"),
            ("kanal",   "Kanal",        "Kanal",  5445,    "1/8 of an Acre"),
            ("marla",   "Marla",        "Marla",  272.25,  "1/20 of a Kanal"),
        ],
    },
    {
        "slug": "andhra-telangana-karnataka",
        "name": "AP, Telangana & Karnataka",
        "short": "South Plains",
        "desc": "The Deccan plateau states commonly use Guntha and Cent for land measurement.",
        "units": [
            ("sqft",    "Square Feet",  "sq ft",  1,       ""),
            ("sqmeter", "Square Meter", "sq m",   10.7639, ""),
            ("gaj",     "Sq Yard (Gaj)", "Gaj",    9,       ""),
            ("acre",    "Acre",         "Acre",   43560,   ""),
            ("hectare", "Hectare",      "ha",     107639,  ""),
            ("cent",    "Cent",         "Cent",   435.6,   "1/100 of an Acre"),
            ("guntha",  "Guntha",       "Guntha", 1089,    "40 Gunthas = 1 Acre"),
            ("ankanam", "Ankanam",      "Ankanam", 72,     "Common in Nellore/Border areas"),
            ("kuncham", "Kuncham",      "Kuncham", 4356,   "Equal to 10 Cents"),
        ],
    },
    {
        "slug": "kerala",
        "name": "Kerala",
        "short": "KL",
        "desc": "Kerala primarily uses Cent and Acre for land measurement.",
        "units": [
            ("sqft",    "Square Feet",  "sq ft",  1,       ""),
            ("sqmeter", "Square Meter", "sq m",   10.7639, ""),
            ("gaj",     "Sq Yard (Gaj)", "Gaj",    9,       ""),
            ("acre",    "Acre",         "Acre",   43560,   ""),
            ("hectare", "Hectare",      "ha",     107639,  ""),
            ("cent",    "Cent",         "Cent",   435.6,   "1/100 of an Acre"),
        ],
    },
    {
        "slug": "assam",
        "name": "Assam",
        "short": "AS",
        "desc": "Assam uses a system similar to West Bengal but with different Katha subdivisions.",
        "units": [
            ("sqft",    "Square Feet",  "sq ft",  1,       ""),
            ("sqmeter", "Square Meter", "sq m",   10.7639, ""),
            ("gaj",     "Sq Yard (Gaj)", "Gaj",    9,       ""),
            ("acre",    "Acre",         "Acre",   43560,   ""),
            ("hectare", "Hectare",      "ha",     107639,  ""),
            ("bigha",   "Bigha",        "Bigha",  14400,   "Same as Bengal Bigha"),
            ("katha",   "Katha",        "Katha",  2880,    "1 Bigha = 5 Kathas in Assam"),
            ("lecha",   "Lecha",        "Lecha",  144,     "1/20 of a Katha"),
        ],
    },
    {
        "slug": "tripura",
        "name": "Tripura",
        "short": "TR",
        "desc": "Tripura uses the Kani as its primary local land measurement unit.",
        "units": [
            ("sqft",    "Square Feet",  "sq ft",  1,       ""),
            ("sqmeter", "Square Meter", "sq m",   10.7639, ""),
            ("gaj",     "Sq Yard (Gaj)", "Gaj",    9,       ""),
            ("acre",    "Acre",         "Acre",   43560,   ""),
            ("hectare", "Hectare",      "ha",     107639,  ""),
            ("kani",    "Kani",         "Kani",   17280,   "Local primary unit"),
        ],
    },
]

# ── Formatting helper ──────────────────────────────────────────────────────────

def fmt(num):
    """Format a number as a human-readable string without exponential notation."""
    if math.isnan(num) or math.isinf(num): return "N/A"
    if num == 0: return "0"
    abs_n = abs(num)
    if abs_n > 0:
        sig = 10
        magnitude = math.floor(math.log10(abs_n))
        rounded = round(num, -int(magnitude) + sig - 1)
    else:
        rounded = num
    abs_r = abs(rounded)
    if abs_r <= 0.000001 and abs_r > 0:
        decimals = max(0, -int(math.floor(math.log10(abs_r))) + 5)
        decimals = min(decimals, 10)
        return f"{rounded:.{decimals}f}".rstrip('0').rstrip('.')
    if abs_r >= 1000:
        if rounded == int(rounded):
            return f"{int(rounded):,}"
        decimals = max(0, min(6, sig - 1 - int(math.floor(math.log10(abs_r)))))
        return f"{rounded:,.{decimals}f}".rstrip('0').rstrip('.')
    if rounded == int(rounded):
        return f"{int(rounded)}"
    return f"{rounded:.6g}"

# ── Nav links ──────────────────────────────────────────────────────────────────

NAV_CATS = [
    ("length","📏 Length"), ("temperature","🌡️ Temperature"), ("area","⬛ Area"),
    ("volume","🧊 Volume"), ("weight","⚖️ Weight"), ("time","⏱️ Time"),
    ("speed","🚀 Speed"), ("pressure","🔵 Pressure"), ("energy","⚡ Energy"),
]

def make_nav_links(active_key="land"):
    links = ""
    for nk, nn in NAV_CATS:
        active = ' class="nav-link active"' if nk == active_key else ' class="nav-link"'
        links += f'<a href="../../{nk}/"{active}>{nn}</a>\n      '
    # Land link
    active = ' class="nav-link active"' if active_key == "land" else ' class="nav-link"'
    links += f'<a href="../../land/"{active}>🌾 Land</a>\n      '
    return links

def make_sidebar_links(active_key="land"):
    links = ""
    for nk, nn in NAV_CATS:
        active = ' active' if nk == active_key else ''
        links += f'<a href="../../{nk}/" class="sidebar-link{active}">{nn} Converter</a>\n          '
    active = ' active' if active_key == "land" else ''
    links += f'<a href="../../land/" class="sidebar-link{active}">🌾 Indian Land Units</a>\n          '
    return links

# ── State page generator ───────────────────────────────────────────────────────

def make_state_page(state):
    slug = state["slug"]
    name = state["name"]
    short = state["short"]
    desc = state["desc"]
    units = state["units"]

    # Build unit options for the select dropdowns
    unit_options = "\n".join(
        f'<option value="{u[0]}">{u[1]} ({u[2]})</option>'
        for u in units
    )

    # Build conversion table (all pairs from sq ft base)
    table_rows = ""
    sqft_unit = next(u for u in units if u[0] == "sqft")
    for u in units:
        if u[0] == "sqft":
            continue
        factor = u[3]  # sq ft per 1 of this unit
        # 1 sq ft = ? this unit
        sqft_to_u = 1 / factor
        # 1 this unit = ? sq ft
        u_to_sqft = factor
        table_rows += f"""<tr>
            <td>1 {u[1]} ({u[2]})</td>
            <td>= {fmt(u_to_sqft)} sq ft</td>
          </tr>
          <tr>
            <td>1 sq ft</td>
            <td>= {fmt(sqft_to_u)} {u[1]} ({u[2]})</td>
          </tr>"""

    # Build JS conversion data
    js_units = "{\n"
    for u in units:
        note = u[4] if len(u) > 4 else ""
        js_units += f'      "{u[0]}": {{ label: "{u[1]}", sym: "{u[2]}", sqft: {u[3]}, note: "{note}" }},\n'
    js_units += "    }"

    # Build unit note list for the info section
    unit_notes_html = ""
    for u in units:
        note = u[4] if len(u) > 4 else ""
        note_str = f" — <em>{note}</em>" if note else ""
        unit_notes_html += f"<li><strong>1 {u[1]} ({u[2]})</strong> = {fmt(u[3])} sq ft{note_str}</li>\n"

    # Related state links
    related_html = ""
    for s in STATES:
        if s["slug"] == slug:
            continue
        related_html += f'<li><a href="../{s["slug"]}-land-conversion/">{s["name"]}</a></li>\n'

    nav_links = make_nav_links("land")
    sidebar_links = make_sidebar_links("land")

    title = f"{name} Land Unit Converter | Bigha, Katha, Acre & More"
    desc_meta = f"Convert land units in {name}: Bigha, Katha, Acre, Square Feet and more. Free online {name} land measurement converter with conversion table."
    canonical = f"https://www.swapunits.online/land/{slug}-land-conversion/"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content="{desc_meta}" />
  <meta name="keywords" content="{name} land converter, {name} bigha to sq ft, land measurement {short}, bigha katha acre converter india" />
  <meta name="robots" content="index, follow" />
  <link rel="canonical" href="{canonical}" />
  <meta property="og:title" content="{name} Land Unit Converter" />
  <meta property="og:description" content="{desc_meta}" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:type" content="website" />
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "WebApplication",
    "name": "{name} Land Unit Converter",
    "url": "{canonical}",
    "description": "{desc_meta}",
    "applicationCategory": "UtilitiesApplication",
    "operatingSystem": "Any",
    "offers": {{"@type": "Offer", "price": "0", "priceCurrency": "USD"}}
  }}
  </script>
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🌾</text></svg>" />
  <link rel="stylesheet" href="../../css/style.css" />
  <!-- Google AdSense -->
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_PUB_ID}" crossorigin="anonymous"></script>
</head>
<body data-category="land">

  <header class="site-header" role="banner">
    <div class="header-inner">
      <a href="/" class="site-logo" aria-label="SwapUnits.online Home">
        Swap<span class="logo-accent">Units</span><span class="logo-tld">.online</span>
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
        <a href="../../land/">Indian Land Units</a> <span>&rsaquo;</span>
        <span>{name}</span>
      </nav>

      <!-- Converter Card -->
      <article class="converter-card pair-page-card">
        <div class="converter-card-header">
          <h1>🌾 {name} Land Unit Converter</h1>
        </div>
        <div class="pair-page-body">
          <p class="pair-intro">{desc}</p>

          <div class="converter-grid">
            <div class="converter-field">
              <label for="land-from-val">From</label>
              <input type="number" id="land-from-val" value="1" placeholder="Enter value" autocomplete="off" />
              <select id="land-from-unit" size="8">
                {unit_options}
              </select>
            </div>
            <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;">
              <button class="swap-btn" id="land-swap-btn" title="Swap units">⇄</button>
            </div>
            <div class="converter-field">
              <label for="land-to-val">To</label>
              <input type="text" id="land-to-val" placeholder="Result" readonly tabindex="-1" />
              <select id="land-to-unit" size="8">
                {unit_options}
              </select>
            </div>
          </div>

          <div class="land-btn-row" style="margin-top: 20px;">
            <button class="pair-convert-btn" id="land-convert-btn">Convert</button>
            <button class="pair-clear-btn" id="land-clear-btn">Clear</button>
          </div>

          <!-- Result display -->
          <div class="land-result-display" id="land-result-display" style="display:none;">
            <div class="land-result-label" id="land-result-label"></div>
            <div class="land-result-value" id="land-result-value"></div>
          </div>
        </div>
      </article>

      <!-- Unit Reference -->
      <section class="pair-info-card">
        <h2>{name} Land Units Reference</h2>
        <ul class="land-unit-list">
          {unit_notes_html}
        </ul>
      </section>

      <!-- Conversion Table -->
      <section class="pair-table-card">
        <h2>{name} Land Unit Conversion Table</h2>
        <table class="pair-table">
          <thead>
            <tr><th>Unit</th><th>Equivalent</th></tr>
          </thead>
          <tbody>
            {table_rows}
          </tbody>
        </table>
      </section>

      <!-- Related States -->
      <section class="pair-related-card">
        <h2>Other Indian State Land Converters</h2>
        <ul class="pair-related-list">
          {related_html}
        </ul>
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
        <div class="site-logo">Swap<span class="logo-accent">Units</span><span class="logo-tld">.online</span></div>
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
          <li><a href="/sitemap.html" style="color:rgba(255,255,255,0.6);text-decoration:none;">Sitemap</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom" style="max-width:1200px;margin:0 auto;padding:20px;border-top:1px solid rgba(255,255,255,0.1);display:flex;justify-content:space-between;font-size:0.8rem;color:rgba(255,255,255,0.45);">
      <span>&copy; 2026 SwapUnits.online &mdash; All rights reserved.</span>
      <span><a href="/privacy.html" style="color:inherit;">Privacy</a> &middot; <a href="/sitemap.html" style="color:inherit;">Sitemap</a></span>
    </div>
  </footer>

  <script>
  (function() {{
    var UNITS = {js_units};

    var fromVal  = document.getElementById('land-from-val');
    var fromUnit = document.getElementById('land-from-unit');
    var toVal    = document.getElementById('land-to-val');
    var toUnit   = document.getElementById('land-to-unit');
    var convBtn  = document.getElementById('land-convert-btn');
    var swapBtn  = document.getElementById('land-swap-btn');
    var clearBtn = document.getElementById('land-clear-btn');
    var resultDisplay = document.getElementById('land-result-display');
    var resultLabel   = document.getElementById('land-result-label');
    var resultValue   = document.getElementById('land-result-value');

    // Default: from sqft, to bigha (or second unit)
    var keys = Object.keys(UNITS);
    fromUnit.value = keys[0];
    toUnit.value   = keys[1] || keys[0];

    function formatNum(n) {{
      if (isNaN(n) || !isFinite(n)) return '';
      if (n === 0) return '0';
      var rounded = parseFloat(n.toPrecision(10));
      var abs = Math.abs(rounded);
      if (abs <= 0.000001 && abs > 0) {{
        var decimals = Math.max(0, Math.min(10, -Math.floor(Math.log10(abs)) + 5));
        return rounded.toFixed(decimals).replace(/\.?0+$/, '');
      }}
      if (abs >= 1) {{
        if (rounded === Math.round(rounded)) return Math.round(rounded).toLocaleString('en-IN');
        // Max 6 decimals for non-integers >= 1
        var dec = Math.max(0, Math.min(6, 9 - Math.floor(Math.log10(abs))));
        return parseFloat(rounded.toFixed(dec)).toLocaleString('en-IN', {{ maximumFractionDigits: 6 }});
      }}
      // Between 0.000001 and 1
      return parseFloat(rounded.toFixed(6)).toString();
    }}

    function doConvert() {{
      var val = parseFloat(String(fromVal.value).replace(/,/g, ''));
      if (isNaN(val)) {{ toVal.value = ''; resultDisplay.style.display = 'none'; return; }}
      var from = fromUnit.value;
      var to   = toUnit.value;
      var fromSqft = UNITS[from].sqft;
      var toSqft   = UNITS[to].sqft;
      var result = val * fromSqft / toSqft;
      var formatted = formatNum(result);
      toVal.value = formatted;
      // Update result display
      resultLabel.textContent = val.toLocaleString('en-IN') + ' ' + UNITS[from].label + ' (' + UNITS[from].sym + ') =';
      resultValue.textContent = formatted + ' ' + UNITS[to].label + ' (' + UNITS[to].sym + ')';
      resultDisplay.style.display = 'flex';
    }}

    fromVal.addEventListener('input', doConvert);
    fromUnit.addEventListener('change', doConvert);
    toUnit.addEventListener('change', doConvert);
    convBtn.addEventListener('click', doConvert);
    clearBtn.addEventListener('click', function() {{
      fromVal.value = '';
      toVal.value = '';
      resultDisplay.style.display = 'none';
    }});
    swapBtn.addEventListener('click', function() {{
      var tmp = fromUnit.value;
      fromUnit.value = toUnit.value;
      toUnit.value = tmp;
      doConvert();
    }});

    doConvert();
  }})();
  </script>

</body>
</html>"""


# ── Land hub page ──────────────────────────────────────────────────────────────

def make_hub_page():
    state_cards = ""
    for s in STATES:
        unit_names = ", ".join(u[1] for u in s["units"] if u[0] not in ("sqft", "sqmeter", "acre", "hectare"))
        state_cards += f"""
        <a href="{s['slug']}-land-conversion/" class="land-state-card">
          <div class="land-state-badge">{s['short']}</div>
          <div class="land-state-name">{s['name']}</div>
          <div class="land-state-units">{unit_names}</div>
        </a>"""

    # Nav for hub page (one level up from state pages)
    nav_links = ""
    for nk, nn in NAV_CATS:
        nav_links += f'<a href="../{nk}/" class="nav-link">{nn}</a>\n      '
    nav_links += '<a href="../land/" class="nav-link active">🌾 Land</a>\n      '

    sidebar_links = ""
    for nk, nn in NAV_CATS:
        sidebar_links += f'<a href="../{nk}/" class="sidebar-link">{nn} Converter</a>\n          '
    sidebar_links += '<a href="../land/" class="sidebar-link active">🌾 Indian Land Units</a>\n          '

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Indian Land Unit Converter | Bigha, Katha, Acre by State | SwapUnits.online</title>
  <meta name="description" content="Free Indian land unit converter for all states. Convert Bigha, Katha, Biswa, Kanal, Marla, Ground, Cent, Guntha and more. State-specific converters for UP, Bihar, Punjab, West Bengal, Rajasthan, MP, Gujarat, Maharashtra, Tamil Nadu, Himachal Pradesh." />
  <meta name="keywords" content="indian land converter, bigha to sq ft, katha to sq ft, land measurement india, bigha calculator, kanal marla converter" />
  <meta name="robots" content="index, follow" />
  <link rel="canonical" href="https://www.unitconvert.net/land/" />
  <meta property="og:title" content="Indian Land Unit Converter by State" />
  <meta property="og:description" content="Convert Indian land units — Bigha, Katha, Kanal, Ground, Cent and more. State-specific converters for all major Indian states." />
  <meta property="og:url" content="https://www.unitconvert.net/land/" />
  <meta property="og:type" content="website" />
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🌾</text></svg>" />
  <link rel="stylesheet" href="../css/style.css?v=2" />
  <!-- Google AdSense -->
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_PUB_ID}" crossorigin="anonymous"></script>
</head>
<body data-category="land">

  <header class="site-header" role="banner">
    <div class="header-inner">
      <a href="/" class="site-logo" aria-label="SwapUnits.online Home">
        Swap<span class="logo-accent">Units</span><span class="logo-tld">.online</span>
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
        <span>Indian Land Units</span>
      </nav>

      <div class="converter-card">
        <div class="converter-card-header">
          <h1>🌾 Indian Land Unit Converter</h1>
        </div>
        <div style="padding: 20px 24px;">
          <p style="color: var(--text-mid); margin-bottom: 24px; line-height: 1.7;">
            Indian land measurement units vary significantly by state. Select your state below to get a
            state-specific converter with the correct local units like Bigha, Katha, Kanal, Ground, Cent, and more.
            All conversions use <strong>Square Feet (sq ft)</strong> as the base unit.
          </p>
          <div class="land-state-grid">
            {state_cards}
          </div>
        </div>
      </div>

      <section class="pair-info-card">
        <h2>Why Land Units Differ by State in India?</h2>
        <p>India's land measurement system evolved independently in different regions over centuries, leading to significant variation. For example, a "Bigha" in Uttar Pradesh (27,000 sq ft) is very different from a Bigha in West Bengal (14,400 sq ft) or Himachal Pradesh (8,712 sq ft). Always verify which state's definition applies before any land transaction.</p>
        <h3 style="margin-top:16px;">Common Units Quick Reference</h3>
        <table class="pair-table" style="margin-top:12px;">
          <thead><tr><th>Unit</th><th>State</th><th>Sq Ft</th></tr></thead>
          <tbody>
            <tr><td>Bigha (Pucca)</td><td>UP / Rajasthan</td><td>27,000 – 27,225</td></tr>
            <tr><td>Bigha</td><td>Bihar</td><td>27,220</td></tr>
            <tr><td>Bigha</td><td>West Bengal</td><td>14,400</td></tr>
            <tr><td>Bigha</td><td>MP</td><td>12,000</td></tr>
            <tr><td>Bigha</td><td>HP / Uttarakhand</td><td>8,712</td></tr>
            <tr><td>Kanal</td><td>Punjab / Haryana</td><td>5,445</td></tr>
            <tr><td>Ground</td><td>Tamil Nadu</td><td>2,400</td></tr>
            <tr><td>Guntha</td><td>Maharashtra / Gujarat</td><td>1,089</td></tr>
            <tr><td>Cent / Decimal</td><td>TN / WB</td><td>435.6</td></tr>
            <tr><td>Acre</td><td>All States</td><td>43,560</td></tr>
          </tbody>
        </table>
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
    <div class="footer-bottom" style="max-width:1200px;margin:0 auto;padding:16px 20px;display:flex;justify-content:space-between;font-size:0.8rem;color:rgba(255,255,255,0.45);">
      <span>&copy; 2026 SwapUnits.online &mdash; All rights reserved.</span>
      <span><a href="/privacy.html">Privacy</a> &middot; <a href="/sitemap.html">Sitemap</a></span>
    </div>
  </footer>

</body>
</html>"""


# ── Generate all pages ─────────────────────────────────────────────────────────

os.makedirs(LAND_DIR, exist_ok=True)

# Hub page
hub_path = os.path.join(LAND_DIR, "index.html")
with open(hub_path, "w", encoding="utf-8") as f:
    f.write(make_hub_page())
print("Generated: land/index.html")

# State pages
sitemap_entries = ["https://www.swapunits.online/land/"]
for state in STATES:
    page_slug = f"{state['slug']}-land-conversion"
    page_dir  = os.path.join(LAND_DIR, page_slug)
    os.makedirs(page_dir, exist_ok=True)
    html = make_state_page(state)
    out_path = os.path.join(page_dir, "index.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    sitemap_entries.append(f"https://www.swapunits.online/land/{page_slug}/")
    print(f"Generated: land/{page_slug}/index.html")

print(f"\nTotal land pages: {len(sitemap_entries)}")


print(f"Sitemap updated with {len(sitemap_entries)} land URLs.")
print("Done! Please run gen_sitemap.py to update sitemap.xml.")

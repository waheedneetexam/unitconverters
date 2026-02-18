"""
gen_category_pages.py
Generates the main category pages (e.g., /length/, /temperature/) with corrected navigation (Emojis + Land).
"""

import os

BASE = r"C:\Users\Administrator\Documents\AntiGravity\Units"
# Adjust BASE if running on linux environment to current directory or relative path
# Since we are in /home/waheed/Work/Anti-Gravity/Units/unitconverters, we can use os.getcwd()
if os.name == 'posix':
    BASE = os.getcwd()

ADSENSE_PUB_ID = "ca-pub-2662293899276634"

CATEGORIES = {
    "length": { "name": "Length", "icon": "📏", "desc": "Convert between meters, feet, miles, and more.", "keywords": "length converter, meter to foot, mile to km" },
    "temperature": { "name": "Temperature", "icon": "🌡️", "desc": "Convert Celsius, Fahrenheit, Kelvin, and more.", "keywords": "temperature converter, celsius to fahrenheit" },
    "area": { "name": "Area", "icon": "⬛", "desc": "Convert square meters, acres, hectares, and more.", "keywords": "area converter, acre to sq ft, hectare to acre" },
    "volume": { "name": "Volume", "icon": "🧊", "desc": "Convert liters, gallons, cups, cubic meters, and more.", "keywords": "volume converter, liter to gallon, cup to ml" },
    "weight": { "name": "Weight", "icon": "⚖️", "desc": "Convert kilograms, pounds, ounces, and more.", "keywords": "weight converter, kg to lbs, grams to ounces" },
    "time": { "name": "Time", "icon": "⏱️", "desc": "Convert seconds, minutes, hours, days, and more.", "keywords": "time converter, seconds to minutes" },
    "speed": { "name": "Speed", "icon": "🚀", "desc": "Convert kph, mph, knots, and more.", "keywords": "speed converter, kph to mph" },
    "pressure": { "name": "Pressure", "icon": "🔵", "desc": "Convert pascal, bar, psi, atmosphere, and more.", "keywords": "pressure converter, bar to psi" },
    "energy": { "name": "Energy", "icon": "⚡", "desc": "Convert joules, calories, kWh, BTU, and more.", "keywords": "energy converter, joule to calorie, btu converter" },
}

NAV_CATS = [
    ("length", "📏 Length"),
    ("temperature", "🌡️ Temperature"),
    ("area", "⬛ Area"),
    ("volume", "🧊 Volume"),
    ("weight", "⚖️ Weight"),
    ("time", "⏱️ Time"),
    ("speed", "🚀 Speed"),
    ("pressure", "🔵 Pressure"),
    ("energy", "⚡ Energy"),
    ("land", "🌾 Land"),
]


ADSENSE_PUB_ID = "ca-pub-2662293899276634"

def make_nav_links(active_key):
    links = ""
    for k, label in NAV_CATS:
        active = ' class="nav-link active"' if k == active_key else ' class="nav-link"'
        # For land, it might be in a different relation if we are not careful, but relative paths ../name/ should work from /name/
        # wait, if we are in /length/, then href="../temperature/" works.
        # But if we use absolute paths /length/ it is safer. 
        # The existing pages use /length/, so let's stick to root-relative or just /name/
        # The sample pair pages used ../, but typical category pages might use /name/
        # Let's check energy/index.html from step 16. It uses /length/.
        links += f'<a href="/{k}/"{active}>{label}</a>\n      '
    return links

def make_sidebar_links(active_key):
    links = ""
    for k, label in NAV_CATS:
        active = ' active' if k == active_key else ''
        cat_name = label.split(' ')[1] # remove emoji
        if k == "land":
            links += f'<a href="/land/" class="sidebar-link{active}">{label} Converter</a>\n          '
        else:
            links += f'<a href="/{k}/" class="sidebar-link{active}">{label} Converter</a>\n          '
    return links

def get_template(cat_key, cat_data):
    name = cat_data["name"]
    icon = cat_data["icon"]
    desc = cat_data["desc"]
    kw = cat_data["keywords"]
    
    nav_html = make_nav_links(cat_key)
    sidebar_html = make_sidebar_links(cat_key)
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title id="page-title">{name} Converter &mdash; Free Online {name} Unit Conversion | SwapUnits.online</title>
  <meta name="description" content="{desc} Free, fast, and accurate." />
  <meta name="keywords" content="{kw}" />
  <meta name="author" content="SwapUnits.online" />
  <meta name="robots" content="index, follow" />
  <link rel="canonical" href="https://www.swapunits.online/{cat_key}/" />
  <meta property="og:type" content="website" />
  <meta property="og:title" content="{name} Converter &mdash; Free Online Tool | SwapUnits.online" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:url" content="https://www.swapunits.online/{cat_key}/" />
  <meta property="og:site_name" content="SwapUnits.online" />
  <meta name="twitter:card" content="summary" />
  <meta name="twitter:title" content="{name} Converter &mdash; SwapUnits.online" />
  <meta name="twitter:description" content="{desc}" />
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "WebApplication",
    "name": "SwapUnits.online &mdash; {name} Converter",
    "url": "https://www.swapunits.online/{cat_key}/",
    "description": "{desc}",
    "applicationCategory": "UtilitiesApplication",
    "operatingSystem": "Any",
    "offers": {{ "@type": "Offer", "price": "0", "priceCurrency": "USD" }}
  }}
  </script>
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>&#x2696;</text></svg>" />
  <link rel="stylesheet" href="../css/style.css" />
  <!-- Google AdSense -->
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_PUB_ID}" crossorigin="anonymous"></script>
</head>
<body data-category="{cat_key}">

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
      {nav_html}
    </div>
  </nav>

  <div class="page-wrapper">
    <main class="main-content" role="main">
      <nav class="breadcrumb" aria-label="Breadcrumb">
        <a href="/">Home</a>
        <span>&rsaquo;</span>
        <span id="breadcrumb-current">{name} Converter</span>
      </nav>

      <article class="converter-card" itemscope itemtype="https://schema.org/WebApplication">
        <div class="converter-card-header">
          <h1 id="converter-title" itemprop="name">{name} Converter</h1>
          <span class="calc-icon" aria-hidden="true">{icon}</span>
        </div>
        <div class="category-tabs" id="category-tabs" role="tablist" aria-label="Unit categories"></div>
        <div class="converter-body" id="converter-body" role="tabpanel"></div>
      </article>

      <div aria-label="Advertisement">
        <!-- In-Content Ad -->
        <ins class="adsbygoogle ad-placeholder in-content"
             style="display:block"
             data-ad-client="{ADSENSE_PUB_ID}"
             data-ad-slot="0987654321"
             data-ad-format="auto"
             data-full-width-responsive="true"></ins>
        <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
      </div>

      <section class="quick-ref" aria-labelledby="quick-ref-title">
        <div class="quick-ref-header" id="quick-ref-title">Quick Reference &mdash; {name}</div>
        <table>
          <thead><tr><th scope="col">From</th><th scope="col">To</th></tr></thead>
          <tbody id="quick-ref-body"></tbody>
        </table>
      </section>

      <section class="seo-content" aria-label="About {name} conversion">
        <h2>About {name} Conversion</h2>
        <p>{desc} Our converter supports all major unit systems including SI (metric), Imperial, and US customary units.</p>
        <p>Simply enter a value, select your source and target units, and get an instant accurate result. Use the swap button to reverse the conversion direction at any time.</p>
        <h2>How to Use the {name} Converter</h2>
        <p>1. Enter your value in the <strong>From</strong> field. 2. Select the source unit from the left dropdown list. 3. Select the target unit from the right dropdown list. 4. The converted result appears instantly in real-time.</p>
      </section>
    </main>

    <aside class="sidebar" role="complementary" aria-label="All converters">
      <div class="sidebar-card">
        <div class="sidebar-card-header">All Converters</div>
        <nav class="sidebar-links" aria-label="All converter categories">
          {sidebar_html}
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
      
      <!-- Popular conversions (static for now, same as energy page example) -->
      <div class="sidebar-card">
        <div class="sidebar-card-header">Popular Conversions</div>
        <div class="popular-grid">
          <div class="popular-item" data-cat="length"      data-from="meter"      data-to="foot"       title="Meters to Feet">m &rarr; ft</div>
          <div class="popular-item" data-cat="length"      data-from="kilometer"  data-to="mile"       title="Kilometers to Miles">km &rarr; mi</div>
          <div class="popular-item" data-cat="temperature" data-from="celsius"    data-to="fahrenheit" title="Celsius to Fahrenheit">&deg;C &rarr; &deg;F</div>
          <div class="popular-item" data-cat="temperature" data-from="fahrenheit" data-to="celsius"    title="Fahrenheit to Celsius">&deg;F &rarr; &deg;C</div>
          <div class="popular-item" data-cat="weight"      data-from="kilogram"   data-to="pound"      title="Kilograms to Pounds">kg &rarr; lb</div>
          <div class="popular-item" data-cat="weight"      data-from="pound"      data-to="kilogram"   title="Pounds to Kilograms">lb &rarr; kg</div>
          <div class="popular-item" data-cat="volume"      data-from="liter"      data-to="usgallon"   title="Liters to Gallons">L &rarr; gal</div>
          <div class="popular-item" data-cat="speed"       data-from="kph"        data-to="mph"        title="km/h to mph">km/h &rarr; mph</div>
          <div class="popular-item" data-cat="area"        data-from="sqmeter"    data-to="sqfoot"     title="m2 to ft2">m&sup2; &rarr; ft&sup2;</div>
          <div class="popular-item" data-cat="energy"      data-from="joule"      data-to="calorie"    title="Joules to Calories">J &rarr; cal</div>
        </div>
      </div>
    </aside>
  </div>

  <footer class="site-footer" role="contentinfo">
    <div class="footer-top">
      <div class="footer-brand">
        <div class="site-logo">Swap<span class="logo-accent">Units</span><span class="logo-tld">.online</span></div>
        <p>Free, fast, and accurate unit conversion for everyone. Supporting all major measurement systems worldwide.</p>
      </div>
      <div class="footer-col">
        <h4>Converters</h4>
        <ul>
          <li><a href="/length/">Length</a></li>
          <li><a href="/temperature/">Temperature</a></li>
          <li><a href="/area/">Area</a></li>
          <li><a href="/volume/">Volume</a></li>
          <li><a href="/weight/">Weight</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>More</h4>
        <ul>
          <li><a href="/time/">Time</a></li>
          <li><a href="/speed/">Speed</a></li>
          <li><a href="/pressure/">Pressure</a></li>
          <li><a href="/energy/">Energy</a></li>
          <li><a href="/land/">Land</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Info</h4>
        <ul>
          <li><a href="/about.html">About</a></li>
          <li><a href="/privacy.html">Privacy Policy</a></li>
          <li><a href="/sitemap.html">Sitemap</a></li>
          <li><a href="/contact.html">Contact</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; 2026 SwapUnits.online &mdash; All rights reserved.</span>
      <span><a href="/privacy.html">Privacy</a> &middot; <a href="/sitemap.html">Sitemap</a></span>
    </div>
  </footer>

  <script src="../js/converters.js?v=2"></script>
  <script src="../js/app.js?v=2"></script>
</body>
</html>"""

def main():
    for cat_key, cat_data in CATEGORIES.items():
        print(f"Generating {cat_key}...")
        html = get_template(cat_key, cat_data)
        
        # Create dir if not exists (should exist)
        cat_dir = os.path.join(BASE, cat_key)
        os.makedirs(cat_dir, exist_ok=True)
        
        out_file = os.path.join(cat_dir, "index.html")
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(html)
            
    print("All category pages generated.")

if __name__ == "__main__":
    main()

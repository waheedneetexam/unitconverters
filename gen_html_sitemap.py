
"""
gen_html_sitemap.py
Generates a visual sitemap page (sitemap.html) similar to unitconverters.net/sitemap.php
"""

import os
from gen_category_pages import NAV_CATS

BASE = os.getcwd()
OUT_FILE = os.path.join(BASE, "sitemap.html")

# Define Categories Groups
GROUPS = {
    "Common Converters": ["length", "weight", "volume", "temperature", "area", "time"],
    "Engineering Converters": ["pressure", "speed", "energy"],
    "Specialized Converters": ["land"]
}

# Map for easy lookup
CAT_MAP = {k: v for k, v in NAV_CATS}

def get_group_html():
    html = ""
    for group_name, cat_keys in GROUPS.items():
        html += f'<div class="sitemap-group">\n'
        html += f'  <h3>{group_name}</h3>\n'
        html += f'  <ul>\n'
        for k in cat_keys:
            if k in CAT_MAP:
                # Remove emoji for clean list
                label = CAT_MAP[k].split(' ', 1)[1] if ' ' in CAT_MAP[k] else CAT_MAP[k]
                html += f'    <li><a href="/{k}/">{label} Converter</a></li>\n'
        html += f'  </ul>\n'
        html += f'</div>\n'
    return html

def main():
    sitemap_grid = get_group_html()
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Sitemap | SwapUnits.online</title>
  <meta name="description" content="Sitemap for SwapUnits.online. Easily navigate to all unit converters." />
  <meta name="robots" content="index, follow" />
  <link rel="canonical" href="https://www.swapunits.online/sitemap.html" />
  
  <!-- Favicon -->
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>⚖️</text></svg>" />
  
  <!-- Styles -->
  <link rel="stylesheet" href="css/style.css" />
  <style>
    .sitemap-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 32px;
        margin-top: 24px;
    }}
    .sitemap-group h3 {{
        font-size: 1.25rem;
        color: var(--blue-dark);
        border-bottom: 2px solid var(--accent);
        padding-bottom: 8px;
        margin-bottom: 16px;
    }}
    .sitemap-group ul {{
        list-style: none;
        padding: 0;
    }}
    .sitemap-group li {{
        margin-bottom: 8px;
    }}
    .sitemap-group a {{
        color: var(--blue-main);
        font-weight: 500;
        text-decoration: none;
        transition: color 0.2s;
    }}
    .sitemap-group a:hover {{
        color: var(--accent);
        text-decoration: underline;
    }}
  </style>
</head>
<body>

  <!-- Header -->
  <header class="site-header" role="banner">
    <div class="header-inner">
      <a href="/" class="site-logo" aria-label="SwapUnits.online Home">
        Swap<span class="logo-accent">Units</span><span class="logo-tld">.online</span>
      </a>
      <span class="header-tagline">Free Online Unit Converter</span>
    </div>
  </header>

  <!-- Nav -->
  <nav class="site-nav" role="navigation" aria-label="Converter categories">
    <div class="nav-inner">
      <a href="/length/" class="nav-link">📏 Length</a>
      <a href="/temperature/" class="nav-link">🌡️ Temperature</a>
      <a href="/area/" class="nav-link">⬛ Area</a>
      <a href="/volume/" class="nav-link">🧊 Volume</a>
      <a href="/weight/" class="nav-link">⚖️ Weight</a>
      <a href="/time/" class="nav-link">⏱️ Time</a>
      <a href="/speed/" class="nav-link">🚀 Speed</a>
      <a href="/pressure/" class="nav-link">🔵 Pressure</a>
      <a href="/energy/" class="nav-link">⚡ Energy</a>
      <a href="/land/" class="nav-link">🌾 Land</a>
    </div>
  </nav>

  <!-- Main -->
  <div class="page-wrapper">
    <main class="main-content" role="main" style="grid-column: 1 / -1;">
      <nav class="breadcrumb" aria-label="Breadcrumb">
        <a href="/">Home</a>
        <span>&rsaquo;</span>
        <span id="breadcrumb-current">Sitemap</span>
      </nav>

      <div class="seo-content" style="margin-top: 0;">
        <h1>Sitemap</h1>
        <p>Navigate easily through all our unit converters.</p>
        
        <div class="sitemap-grid">
            {sitemap_grid}
        </div>
      </div>
    </main>
  </div>

  <!-- Footer -->
  <footer class="site-footer" role="contentinfo">
    <div class="footer-top">
      <div class="footer-brand">
        <div class="site-logo">Swap<span class="logo-accent">Units</span><span class="logo-tld">.online</span></div>
        <p>Free, fast, and accurate unit conversion for everyone.</p>
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
      <span>&copy; 2026 SwapUnits.online — All rights reserved.</span>
      <span>
        <a href="/privacy.html">Privacy</a> ·
        <a href="/sitemap.xml">XML Sitemap</a>
      </span>
    </div>
  </footer>

</body>
</html>"""

    with open(OUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"Generated {OUT_FILE}")

if __name__ == "__main__":
    main()

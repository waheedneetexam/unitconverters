"""
gen_sitemap.py
Generates a clean sitemap.xml by crawling the current directory for HTML files.
Includes:
- Homepage
- Static pages (about.html, privacy.html)
- Category pages
- Pair pages
- Land pages
"""

import os
import datetime

BASE_URL = "https://www.swapunits.online"
BASE_DIR = os.getcwd()

# Priorities
PRIORITY_HOME = "1.0"
PRIORITY_MAIN = "0.8"   # Categories, About, Privacy
PRIORITY_LAND = "0.8"   # Land Hub
PRIORITY_PAGE = "0.7"   # Pair pages, Land state pages

def get_files():
    urls = []
    
    # 1. Static & Root pages
    static_pages = [
        ("index.html",   "/",            PRIORITY_HOME),
        ("about.html",   "/about.html",  PRIORITY_MAIN),
        ("privacy.html", "/privacy.html", PRIORITY_MAIN),
    ]

    for filename, path, prio in static_pages:
        if os.path.exists(os.path.join(BASE_DIR, filename)):
            urls.append({
                "loc": f"{BASE_URL}{path}",
                "lastmod": datetime.date.today().isoformat(),
                "priority": prio
            })

    # 2. Crawl for index.html in subdirectories
    for root, dirs, files in os.walk(BASE_DIR):
        if "index.html" in files:
            rel_path = os.path.relpath(root, BASE_DIR)
            if rel_path == ".":
                continue # Already handled root index.html
            
            # Skip hidden folders or non-content
            if rel_path.startswith(".") or "__" in rel_path:
                continue

            # Construct URL
            # Only support folders that directly map to URL segments
            # e.g. /length/ -> https://.../length/
            # e.g. /length/meter-to-foot/ -> https://.../length/meter-to-foot/
            
            url_path = rel_path.replace("\\", "/") + "/"
            
            # Determine priority
            # Top level categories (e.g. length, weight, land)
            is_top_level = "/" not in url_path.strip("/")
            priority = PRIORITY_MAIN if is_top_level else PRIORITY_PAGE
            
            urls.append({
                "loc": f"{BASE_URL}/{url_path}",
                "lastmod": datetime.date.today().isoformat(),
                "priority": priority
            })
            
    return urls

def generate_sitemap(urls):
    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">')
    
    for u in urls:
        xml.append('  <url>')
        xml.append(f'    <loc>{u["loc"]}</loc>')
        xml.append(f'    <lastmod>{u["lastmod"]}</lastmod>')
        xml.append('    <changefreq>monthly</changefreq>')
        xml.append(f'    <priority>{u["priority"]}</priority>')
        xml.append('  </url>')
        
    xml.append('</urlset>')
    return "\n".join(xml)

if __name__ == "__main__":
    print("Scanning directory for sitemap generation...")
    urls = get_files()
    print(f"Found {len(urls)} URLs.")
    
    xml_content = generate_sitemap(urls)
    
    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write(xml_content)
        
    print("sitemap.xml created successfully.")

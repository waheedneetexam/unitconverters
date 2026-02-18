import os

base = r'C:\Users\Administrator\Documents\AntiGravity\Units'
required = [
    'index.html', 'css/style.css', 'js/converters.js', 'js/app.js',
    'length/index.html', 'temperature/index.html', 'area/index.html',
    'volume/index.html', 'weight/index.html', 'time/index.html',
    'speed/index.html', 'pressure/index.html', 'energy/index.html',
    'sitemap.xml', 'robots.txt', 'ads.txt', '.htaccess', 'README.md'
]

print('=== File Verification ===')
all_ok = True
for f in required:
    path = os.path.join(base, f)
    exists = os.path.exists(path)
    size = os.path.getsize(path) if exists else 0
    status = 'OK' if exists else 'MISSING'
    print(f'  [{status}] {f} ({size:,} bytes)')
    if not exists:
        all_ok = False

print()
print('=== SEO Check (index.html) ===')
with open(os.path.join(base, 'index.html'), encoding='utf-8') as fh:
    content = fh.read()

checks = {
    'title tag': '<title' in content,
    'meta description': 'name="description"' in content,
    'canonical URL': 'rel="canonical"' in content,
    'JSON-LD': 'application/ld+json' in content,
    'Open Graph': 'og:title' in content,
    'Twitter Card': 'twitter:card' in content,
    'AdSense slot': 'adsbygoogle' in content,
    'sitemap link': 'sitemap.xml' in content,
}
for check, result in checks.items():
    print(f'  [{"OK" if result else "FAIL"}] {check}')

print()
print('All files present!' if all_ok else 'Some files missing!')

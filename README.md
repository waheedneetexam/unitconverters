# UnitConvert.net — Unit Converter Website

A free, fast, and SEO-optimized unit converter website built with pure HTML, CSS, and JavaScript. No frameworks, no build tools — just open and host.

## Features

- **9 Converter Categories**: Length, Temperature, Area, Volume, Weight, Time, Speed, Pressure, Energy
- **Real-time conversion** with instant results as you type
- **Swap button** to reverse conversion direction
- **Copy to clipboard** button for results
- **Quick Reference Table** for each category
- **Premium dark-green design** with responsive mobile layout
- **Full SEO**: unique titles, meta descriptions, JSON-LD structured data per page
- **Google AdSense ready**: placeholder slots in header, sidebar, and in-content positions
- **Server-ready**: Apache `.htaccess` with gzip, caching, and security headers

## File Structure

```
Units/
├── index.html              # Homepage
├── css/style.css           # All styles
├── js/
│   ├── converters.js       # Conversion math
│   └── app.js              # UI logic
├── length/index.html       # Length converter page
├── temperature/index.html  # Temperature converter page
├── area/index.html         # Area converter page
├── volume/index.html       # Volume converter page
├── weight/index.html       # Weight converter page
├── time/index.html         # Time converter page
├── speed/index.html        # Speed converter page
├── pressure/index.html     # Pressure converter page
├── energy/index.html       # Energy converter page
├── sitemap.xml             # Google sitemap
├── robots.txt              # Search engine rules
├── ads.txt                 # Google AdSense declaration
└── .htaccess               # Apache server config
```

## Hosting

### Option 1: Apache (cPanel, WAMP, XAMPP)
1. Upload the entire `Units/` folder to your server's `public_html/` directory
2. The `.htaccess` file handles clean URLs, gzip, and caching automatically
3. Enable `mod_rewrite` and `mod_deflate` in Apache if not already enabled

### Option 2: Nginx
Add this to your Nginx server block:
```nginx
server {
    root /var/www/html/Units;
    index index.html;
    
    location / {
        try_files $uri $uri/ $uri/index.html =404;
    }
    
    gzip on;
    gzip_types text/html text/css application/javascript;
    
    location ~* \.(css|js)$ {
        expires 30d;
        add_header Cache-Control "public, max-age=2592000";
    }
}
```

### Option 3: GitHub Pages
1. Push the `Units/` folder to a GitHub repository
2. Go to Settings → Pages → Source: Deploy from branch
3. Select `main` branch and `/` (root) or `/docs` folder
4. Your site will be live at `https://username.github.io/repo-name/`

### Option 4: Netlify / Vercel
1. Drag and drop the `Units/` folder to [netlify.com/drop](https://netlify.com/drop)
2. Your site is instantly live with a free HTTPS URL

### Option 5: Local Testing
Simply open `index.html` in any browser — no server needed for local testing.

## Monetization Setup (Google AdSense)

1. **Apply for AdSense**: Go to [adsense.google.com](https://adsense.google.com) and apply
2. **Get your Publisher ID**: It looks like `ca-pub-1234567890123456`
3. **Update ads.txt**: Replace `XXXXXXXXXXXXXXXX` in `ads.txt` with your Publisher ID
4. **Activate ad slots**: In each HTML file, uncomment the `<ins class="adsbygoogle">` blocks and replace `ca-pub-XXXXXXXXXXXXXXXX` with your Publisher ID
5. **Replace data-ad-slot values**: Get real slot IDs from your AdSense dashboard

### Ad Slot Locations (per page)
| Position | Size | AdSense Format |
|----------|------|----------------|
| Header banner | 728×90 | Leaderboard |
| Sidebar | 300×250 | Medium Rectangle |
| In-content | Responsive | Auto |

## SEO Checklist

- [x] Unique `<title>` per page
- [x] Unique `<meta description>` per page
- [x] `<meta keywords>` per page
- [x] Open Graph tags for social sharing
- [x] Twitter Card meta tags
- [x] JSON-LD structured data (WebApplication schema)
- [x] Canonical URLs
- [x] `sitemap.xml` with all pages
- [x] `robots.txt` with sitemap reference
- [x] Semantic HTML5 (header, nav, main, aside, footer, article, section)
- [x] ARIA labels for accessibility
- [x] Responsive mobile design

### After Hosting — Submit to Google
1. Go to [Google Search Console](https://search.google.com/search-console)
2. Add your domain and verify ownership
3. Submit your sitemap: `https://yourdomain.com/sitemap.xml`

## Customization

### Change Domain
Replace all instances of `https://www.unitconvert.net/` in:
- All HTML files (canonical URLs, OG tags, JSON-LD)
- `sitemap.xml`
- `robots.txt`

### Add More Converters
1. Add a new entry to `CONVERTERS` object in `js/converters.js`
2. Create a new folder (e.g., `power/`) with an `index.html` (copy from any category page)
3. Add the new category to the nav bar in all HTML files
4. Add the URL to `sitemap.xml`

## License
Free to use and modify for personal and commercial projects.

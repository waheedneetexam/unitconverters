"""
update_conv_links.py
Updates conv-link hrefs in index.html to point to individual pair pages.
"""
import re, os

BASE = r"C:\Users\Administrator\Documents\AntiGravity\Units"

# Exact slug map for each conv-link in index.html
# (cat, from_id, to_id) -> (from_slug, to_slug)
SLUG_MAP = {
    # length
    ("length","centimeter","inch"):       ("centimeter","inch"),
    ("length","millimeter","inch"):       ("millimeter","inch"),
    ("length","meter","foot"):            ("meter","foot"),
    ("length","kilometer","mile"):        ("kilometer","mile"),
    ("length","centimeter","foot"):       ("centimeter","foot"),
    ("length","inch","foot"):             ("inch","foot"),
    ("length","meter","yard"):            ("meter","yard"),
    ("length","inch","centimeter"):       ("inch","centimeter"),
    ("length","inch","millimeter"):       ("inch","millimeter"),
    ("length","foot","meter"):            ("foot","meter"),
    ("length","mile","kilometer"):        ("mile","kilometer"),
    ("length","foot","centimeter"):       ("foot","centimeter"),
    ("length","foot","inch"):             ("foot","inch"),
    ("length","yard","meter"):            ("yard","meter"),
    # weight
    ("weight","kilogram","pound"):        ("kilogram","pound"),
    ("weight","gram","ounce"):            ("gram","ounce"),
    ("weight","pound","ounce"):           ("pound","ounce"),
    ("weight","pound","kilogram"):        ("pound","kilogram"),
    ("weight","ounce","gram"):            ("ounce","gram"),
    ("weight","ounce","pound"):           ("ounce","pound"),
    # temperature
    ("temperature","celsius","fahrenheit"):   ("celsius","fahrenheit"),
    ("temperature","fahrenheit","celsius"):   ("fahrenheit","celsius"),
    # volume
    ("volume","liter","usgallon"):        ("liter","us-gallon"),
    ("volume","milliliter","uscup"):      ("milliliter","us-cup"),
    ("volume","usgallon","liter"):        ("us-gallon","liter"),
    ("volume","uscup","milliliter"):      ("us-cup","milliliter"),
    # speed
    ("speed","mph","kph"):                ("mile-per-hour","kilometer-per-hour"),
    ("speed","kph","mph"):                ("kilometer-per-hour","mile-per-hour"),
    # area
    ("area","acre","sqfoot"):             ("acre","square-foot"),
    ("area","sqfoot","acre"):             ("square-foot","acre"),
}

index_path = os.path.join(BASE, "index.html")
with open(index_path, encoding="utf-8") as f:
    content = f.read()

def replace_href(m):
    full = m.group(0)
    cat  = re.search(r'data-cat="([^"]+)"', full).group(1)
    frm  = re.search(r'data-from="([^"]+)"', full).group(1)
    to   = re.search(r'data-to="([^"]+)"', full).group(1)
    key  = (cat, frm, to)
    if key in SLUG_MAP:
        fs, ts = SLUG_MAP[key]
        href = f"{cat}/{fs}-to-{ts}/"
        return full.replace('href="#"', f'href="{href}"')
    return full

orig_count = content.count('href="#" class="conv-link"')
new_content = re.sub(r'<a href="#" class="conv-link"[^>]+>', replace_href, content)
new_count = new_content.count('href="#" class="conv-link"')

print(f"Links updated: {orig_count - new_count} of {orig_count}")

with open(index_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print("index.html updated successfully.")

# Also verify a sample page exists
sample = os.path.join(BASE, "volume", "us-gallon-to-liter", "index.html")
print(f"Sample page exists: {os.path.exists(sample)}")
print(f"  -> {sample}")

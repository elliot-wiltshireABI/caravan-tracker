import requests
from bs4 import BeautifulSoup
from datetime import datetime

# =====================
# List of URLs to track
# =====================
URLS = [
    "https://ladrambay.co.uk/ownership/",
    "https://www.beverleyholidayhomes.co.uk/homes/",
    "https://harlynsands.co.uk/holiday-homes-for-sale/",
    "https://www.durdledoor.co.uk/sales",
    "https://www.newlandsholidays.co.uk/holiday-home-sales",
    "https://www.shorefield.co.uk/ownership/results?park=&min_bedrooms=&max_bedrooms=&min_price=&max_price=",
    "https://www.freshwaterbeach.co.uk/static-caravans-for-sale-in-dorset",
    "https://meadow-lakes.co.uk/ownership/for-sale/",
]

# =====================
# Function to scrape each site
# =====================
def scrape_site(url):
    try:
        r = requests.get(url, headers={"User-Agent":"Mozilla/5.0"}, timeout=30)
        r.raise_for_status()
    except:
        return []
    soup = BeautifulSoup(r.text, "html.parser")
    listings = []

    # Generic scraping: look for headings and price symbols
    for card in soup.find_all(["div","article"], class_=True):
        text = card.get_text(strip=True)
        if "£" in text:
            name_tag = card.find(["h2","h3","h4"])
            if name_tag:
                name = name_tag.get_text(strip=True)
                price_start = text.find("£")
                price = text[price_start:price_start+15].split()[0]
                listings.append(f"{name} – {price}")
    return listings

# =====================
# Generate HTML report
# =====================
def generate_html(all_listings):
    html = f"<html><body style='font-family:Arial;'>"
    html += f"<h2>Weekly Caravan Sales Report</h2>"
    html += f"<p>Date: {datetime.now().strftime('%d %B %Y')}</p>"
    html += "<hr>"
    for url, listings in all_listings.items():
        html += f"<h3>{url}</h3><ul>"
        for item in listings:
            html += f"<li>{item}</li>"
        html += "</ul>"
    html += "</body></html>"
    return html

# =====================
# Main function
# =====================
def main():
    all_listings = {}
    for url in URLS:
        listings = scrape_site(url)
        all_listings[url] = listings
    html = generate_html(all_listings)

    # Save HTML file for GitHub Action email
    with open("report.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Report generated successfully.")

if __name__ == "__main__":
    main()

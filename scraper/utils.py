import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin
from .models import ScrapedItem

# Base URL of the FinCEN website
BASE_URL = "https://www.fincen.gov"


# Parse various date formats like MM/DD/YYYY or MM-DD-YYYY
def parse_date(text):
    for fmt in ["%m/%d/%Y", "%m-%d-%Y"]:
        try:
            return datetime.strptime(text.strip(), fmt).date()
        except:
            continue
    return None


# Extract date and optional hyperlink (if present) from a table cell
def extract_date_url(cell):
    a = cell.find("a")
    if a:
        return parse_date(a.text), urljoin(BASE_URL, a["href"])
    elif cell.text.strip() and cell.text.strip() != "---":
        return parse_date(cell.text), None  # just a plain date, no link
    return None, None  


# Main scraping function
def scrape_fincen():
    url = f"{BASE_URL}/resources/statutes-and-regulations/special-measures"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Locate the table
    table = soup.find("table", id="special-measures-table")
    rows = table.find_all("tr")[1:]  # skip header row

    # Current DB entries (used to detect removed items)
    previous_names = set(ScrapedItem.objects.values_list('name', flat=True))
    current_names = set()

    added = []   # to track newly added institutions
    removed = [] # to track removed institutions

    # Process each row
    for row in rows:
        cells = row.find_all("td")
        if len(cells) != 5:
            continue  # skip if table row is corrupted

        name = cells[0].text.strip()
        current_names.add(name)

        # Extract all fields with their date + URL (if available)
        finding_date, finding_url = extract_date_url(cells[1])
        nprm_date, nprm_url = extract_date_url(cells[2])
        final_rule_date, final_rule_url = extract_date_url(cells[3])
        rescinded_date, rescinded_url = extract_date_url(cells[4])

        # Insert or update the row
        obj, created = ScrapedItem.objects.update_or_create(
            name=name,
            defaults={
                "finding_date": finding_date,
                "finding_url": finding_url,
                "nprm_date": nprm_date,
                "nprm_url": nprm_url,
                "final_rule_date": final_rule_date,
                "final_rule_url": final_rule_url,
                "rescinded_date": rescinded_date,
                "rescinded_url": rescinded_url,
            }
        )
        if created:
            added.append(name)  # New item added

    # Determine which old items are now missing
    removed = list(previous_names - current_names)
    ScrapedItem.objects.filter(name__in=removed).delete()  # Remove them

    # Return the changes to the caller (view)
    return {
        "added": added,
        "removed": removed
    }

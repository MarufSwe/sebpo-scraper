# SEBPO Scraper Project

This Django-based web scraper automatically collects, displays, and tracks changes in the **FinCEN Special Measures Table** from the U.S. Treasury website.

---

## ✅ How the scraper works

- The scraping logic is implemented using `requests` + `BeautifulSoup` 
- The script parses each row in the FinCEN table and saves the data in the PostgreSQL database using Django ORM.
- The scraping logic is placed inside a Django **management command**:
  
scraper/management/commands/scrape_fincen.py
## It can be run manually:

```bash
python manage.py scrape_fincen


## 🔁 How the refresh button works
- A 🔄 Refresh button is available in the UI.
- When clicked, it sends an AJAX POST request to a Django view.
- The view re-runs the scraping logic and compares new vs old data.
- Any added or removed rows are shown inside a Bootstrap modal without reloading the page.


## 📋 How differences are displayed
After scraping:

- ✅ New items are shown in green with the label "🟢 New Items"
- ❌ Removed items are shown in red with the label "🔴 Removed Items"
- ✅ If no change is detected, the modal shows "No changes in the table."


## 🔐 How authentication is enforced
- All views are protected with Django’s built-in login system.
- You must log in to access the data table or perform scraping actions.

## ⏰ How to set up scheduled scraping (cron)
To scrape the FinCEN table automatically every day at 3 AM, add this cron job:

```bash
0 3 * * * /home/user/sebpo-scraper/venv/bin/python /home/user/sebpo-scraper/manage.py scrape_fincen >> /home/user/sebpo-scraper/logs/scrape.log 2>&1


## 🚀 Deployment
Full step-by-step production deployment instructions are available in the file: scraper/deployment_guide.md



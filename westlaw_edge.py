from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

SEARCH_TERMS = [
    {"party": "Acme Corp", "court": "Federal", "state": "California"},
    {"party": "Smith v. Jones", "court": "Federal", "state": "New York"},
]
OUTPUT_FILE = "docket_results.csv"

def launch_westlaw():
    """Launch browser and navigate to Westlaw Edge."""
    driver = webdriver.Chrome()  
    driver.get("https://1.next" + ".westlaw.com")  
    input()
    return driver

def navigate_to_dockets(driver):
    try:
        dockets_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Dockets"))
        )
        dockets_link.click()
        time.sleep(2)
    except Exception as e:
        print(f"Navigation error: {e}")
        print("Try navigating manually to: Dockets section")

def search_docket(driver, party="", case_number="", court="", state=""):
    try:
        if party:
            party_field = driver.find_element(By.ID, "searchInputId")
            party_field.clear()
            party_field.send_keys(party)

        search_btn = driver.find_element(By.ID, "searchButton")
        search_btn.click()
        time.sleep(3)

    except Exception as e:
        print(f"Search error: {e}")

def collect_results(driver):
    results = []
    try:
        items = driver.find_elements(By.CSS_SELECTOR, ".result-item")
        for item in items:
            title = item.find_element(By.CSS_SELECTOR, ".title").text
            court = item.find_element(By.CSS_SELECTOR, ".court").text
            date = item.find_element(By.CSS_SELECTOR, ".date").text
            results.append({"title": title, "court": court, "date": date})
    except Exception as e:
        print(f"Collection error: {e}")
    return results

def save_results(all_results, filename):
    """Save results to CSV."""
    if not all_results:
        print("No results to save.")
        return
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=all_results[0].keys())
        writer.writeheader()
        writer.writerows(all_results)
    print(f"Saved {len(all_results)} results to {filename}")

if __name__ == "__main__":
    driver = launch_westlaw()
    navigate_to_dockets(driver)

    all_results = []
    for term in SEARCH_TERMS:
        print(f"Searching: {term}")
        search_docket(driver, party=term.get("party", ""))
        results = collect_results(driver)
        all_results.extend(results)
        time.sleep(2)

    save_results(all_results, OUTPUT_FILE)
    driver.quit()

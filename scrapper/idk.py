from playwright.sync_api import sync_playwright
import json

def scrape_postcode_data(postcode):
    with sync_playwright() as p:
        # Launch a headless browser
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Open the target website
        page.goto("https://www.utilitybidder.co.uk/business-gas/")
        
        # Wait for the cookie consent button and click it if it exists
        try:
            page.wait_for_selector('#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll', timeout=5000)
            page.click('#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll')
        except Exception as e:
            print(f"Error handling cookies: {e}")

        # Input the postcode
        page.fill('#address', postcode)

        # Click the "Compare Prices" button
        page.click('#search')

        # Wait for the results to load
        page.wait_for_selector('#addressSelect', timeout=10000)

        # Extract all options from the select field
        options = page.query_selector_all('#addressSelect option')

        # Format the options as a list of dictionaries for JSON response
        option_data = [{"address": option.inner_text()} for option in options[1:]]  # Skip the first option (usually the placeholder)

        # Close the browser
        browser.close()

        return option_data

# Example usage
postcode = 'SW1A 1AA'  # Replace with the desired postcode
data = scrape_postcode_data(postcode)
print(json.dumps(data, indent=2))

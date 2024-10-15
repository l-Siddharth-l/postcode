# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import json

# def scrape_postcode_data(postcode):
#     # Configure Selenium WebDriver for headless mode
#     chrome_options = Options()
#     chrome_options.add_argument("--headless")
#     chrome_options.add_argument("--disable-gpu")
#     chrome_options.add_argument("--no-sandbox")
#     chrome_options.add_argument("--disable-dev-shm-usage")
#     chrome_options.add_argument("--disable-software-rasterizer")
#     chrome_options.add_argument("--window-size=1920x1080")
#     chrome_options.add_argument("--disable-extensions")
#     chrome_options.add_argument("--disable-automation")
#     chrome_options.add_argument("--log-level=3")

#     # Initialize WebDriver
#     driver = webdriver.Chrome(options=chrome_options)

#     # Open the target website
#     driver.get("https://www.utilitybidder.co.uk/business-gas/")

#     # Handle cookie consent if it appears
#     try:
#         cookie_button = WebDriverWait(driver, 5).until(
#             EC.element_to_be_clickable((By.ID, 'CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll'))
#         )
#         cookie_button.click()
#     except Exception:
#         pass

#     # Input the postcode
#     postcode_field = driver.find_element(By.ID, 'address')
#     postcode_field.send_keys(postcode)

#     # Click the "Compare Prices" button
#     compare_button = driver.find_element(By.XPATH, '//button[@id="search"]')
#     compare_button.click()

#     # Wait for the results to load
#     WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'addressSelect')))

#     # Extract all options from the select field
#     select_element = driver.find_element(By.ID, 'addressSelect')
#     options = select_element.find_elements(By.TAG_NAME, 'option')

#     # Format the options as a list of dictionaries for JSON response
#     option_data = [{"address": option.text} for option in options[1:]]

#     # Close the browser
#     driver.quit()

#     return option_data


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

# # Example usage
# postcode = 'SW1A 1AA'  # Replace with the desired postcode
# data = scrape_postcode_data(postcode)
# print(json.dumps(data, indent=2))

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time

# Presentation delay (adjust this)
STEP_DELAY = 1.5  

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

BASE_URL = "http://127.0.0.1:5000"

print("Opening KB List Page...")
driver.get(BASE_URL)
time.sleep(STEP_DELAY)

wait.until(EC.presence_of_element_located((By.TAG_NAME, "ul")))

kb_links = driver.find_elements(By.TAG_NAME, "a")
kb_urls = [link.get_attribute("href") for link in kb_links]

print(f"Found {len(kb_urls)} KB articles")

for index, url in enumerate(kb_urls, start=1):

    print(f"\nProcessing KB {index}...")
    driver.get(url)
    time.sleep(STEP_DELAY)

    wait.until(EC.presence_of_element_located((By.ID, "validTo")))

    # 1 Update Date
    next_year = datetime.now().year + 1
    new_date = f"{next_year}-12-31"

    print("Updating Valid To date...")
    valid_to = driver.find_element(By.ID, "validTo")
   
    driver.execute_script("""
    arguments[0].value = arguments[1];
    """, valid_to, new_date)
    
    time.sleep(STEP_DELAY)

    #  Handle Attachments
    attachments = driver.find_elements(By.CLASS_NAME, "attachment-link")

    attachment_text = "No attachments available."

    if attachments:
        print("Attachment found. Processing...")
        attachment = attachments[0]
        file_name = attachment.text
        file_url = attachment.get_attribute("href")

        attachment_html = f'<a href="{file_url}" target="_blank">{file_name}</a>'
        driver.execute_script("""
            var row = arguments[0].closest("p");
            if (row) row.remove();
        """, attachment)

        time.sleep(STEP_DELAY)

        disclaimer_html = f"""
            <div id="autoDisclaimer" style="
                border:1px solid #ccc;
                margin-top:20px;
                border-radius:6px;
                overflow:hidden;
                font-family: Arial, sans-serif;
            ">


                <div style="
                    background-color:#1e3c72;
                    color:white;
                    padding:15px;
                    font-size:14px;
                    line-height:1.6;
                ">
                    <h3 style="margin-top:0;">Attachments</h3>
                    <b>Disclaimer:</b><br><br>

                    For the most accurate and up-to-date information, please avoid 
                    bookmarking the attachment link directly. As best practice, always 
                    access attachments through the corresponding knowledge article.

                    <br><br>

                    This ensures you are viewing the latest version and helps prevent 
                    outdated or incorrect references.
                </div>

                <!-- White Section BELOW Header -->
                <div style="
                    padding:15px;
                    background-color:white;
                    color:#333;
                    font-size:14px;
                ">
                    {attachment_html}
                </div>

            </div>
            """

        attachments_div = driver.find_element(By.ID, "attachments")
        driver.execute_script("""
            arguments[0].insertAdjacentHTML('afterend', arguments[1]);
        """, attachments_div, disclaimer_html)

        time.sleep(STEP_DELAY)

    else:
        print("No attachments found.")

    #  Insert Disclaimer
    
    time.sleep(STEP_DELAY)

    # Publish
    print("Publishing KB...")
    publish_button = driver.find_element(By.ID, "publishButton")
    publish_button.click()

    time.sleep(2)

print("\nAll KBs processed successfully!")
time.sleep(2)
driver.quit()

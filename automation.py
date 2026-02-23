from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time

STEP_DELAY = 1.5

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

BASE_URL = "http://127.0.0.1:5000"

print("Opening KB List Page...")
driver.get(BASE_URL)

# Wait for table to load
wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
time.sleep(STEP_DELAY)

# Get only KB number links (not all <a> tags)
kb_links = driver.find_elements(By.XPATH, "//table//a")

kb_urls = [link.get_attribute("href") for link in kb_links]

print(f"Found {len(kb_urls)} KB articles")

for index, url in enumerate(kb_urls, start=1):

    print(f"\nProcessing KB {index}...")
    driver.get(url)

    wait.until(EC.presence_of_element_located((By.ID, "validTo")))
    time.sleep(STEP_DELAY)

    # -------------------------
    # 1️⃣ Update Valid To Date
    # -------------------------
    next_year = datetime.now().year + 1
    new_date = f"{next_year}-12-31"

    print("Updating Valid To date...")

    valid_to = driver.find_element(By.ID, "validTo")

    # Highlight field
    driver.execute_script(
        "arguments[0].style.border='2px solid green';", valid_to
    )
    time.sleep(1)

    # Set value via JS (stable way)
    driver.execute_script(
        "arguments[0].value = arguments[1];",
        valid_to,
        new_date
    )

    time.sleep(STEP_DELAY)

    # -------------------------
    # 2️⃣ Handle Attachments
    # -------------------------
    attachments = driver.find_elements(By.CLASS_NAME, "attachment-link")

    if attachments:

        print("Attachment found. Processing...")

        attachment = attachments[0]
        file_name = attachment.text
        file_url = attachment.get_attribute("href")

        attachment_html = f'<a href="{file_url}" target="_blank">{file_name}</a>'

        # Remove only the attachment row (keep heading)
        driver.execute_script("""
            var row = arguments[0].closest("p");
            if (row) row.remove();
        """, attachment)

        time.sleep(STEP_DELAY)

        # Build disclaimer block
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
                <b>Disclaimer:</b><br><br>

                For the most accurate and up-to-date information, 
                please avoid bookmarking the attachment link directly.
                Always access attachments through the corresponding 
                knowledge article.

                <br><br>

                This ensures you are viewing the latest version 
                and prevents outdated references.
            </div>

            <div style="
                padding:15px;
                background-color:white;
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

    # -------------------------
    # 3️⃣ Publish
    # -------------------------
    print("Publishing KB...")

    publish_button = driver.find_element(By.ID, "publishButton")

    driver.execute_script(
        "arguments[0].style.backgroundColor='#28a745';",
        publish_button
    )

    time.sleep(1)
    publish_button.click()

    time.sleep(2)

print("\nAll KBs processed successfully!")
time.sleep(2)
driver.quit()

# import fitz  # PyMuPDF
# def convert_pdf_to_html(self, input_path, output_path):

#     if not os.path.exists(input_path):
#         raise FileNotFoundError(f"Input file not found: {input_path}")

#     os.makedirs(os.path.dirname(output_path), exist_ok=True)

#     # Create temp directory (same as DOC)
#     self.temp_dir = tempfile.mkdtemp()

#     temp_html = os.path.join(self.temp_dir, "temp_pdf.html")

#     print(f"[INFO] Converting PDF: {input_path}")

#     doc = fitz.open(input_path)

#     html_content = ""
#     for page in doc:
#         html_content += page.get_text("html")

#     doc.close()

#     with open(temp_html, "w", encoding="utf-8") as f:
#         f.write(html_content)

#     # 👇 IMPORTANT: Reuse your existing cleaning pipeline
#     self.clean_and_preserve_tables(temp_html, output_path)

#     print(f"[SUCCESS] PDF converted to HTML: {output_path}")
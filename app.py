from flask import Flask, render_template, redirect, url_for
from datetime import datetime

print("APP FILE IS RUNNING")
app = Flask(__name__)


# Dummy KB Data
kb_data = [
    {
        "id": 1,
        "kb_number": "KB001",
        "title": "How to Reset Password",
        "author": "Moulika",
        "category": "Access Management",
        "valid_to": "2025-12-31",
        "body": "This article explains how to reset your password.",
        "attachments": [
            {
                "name": "Password_Reset_Guide.pdf",
                "url": "https://example.com/password_reset.pdf"
            }
        ]
    },
    {
        "id": 2,
        "kb_number": "KB002",
        "title": "How to Update Profile Information",
        "author": "Moulika",
        "category": "User Management",
        "valid_to": "2025-12-29",
        "body": "This article explains how to update your profile information.",
        "attachments": [
            {
                "name": "Profile_Update_Guide.pdf",
                "url": "https://example.com/profile_update.pdf"
            }
        ]
    }
]

@app.route("/")
def kb_list():
    return render_template("kb_list.html", kb_data=kb_data)

@app.route("/kb/<int:kb_id>")
def kb_detail(kb_id):
    kb = next((item for item in kb_data if item["id"] == kb_id), None)
    return render_template("kb_detail.html", kb=kb)

@app.route("/publish/<int:kb_id>")
def publish_kb(kb_id):
    print(f"KB {kb_id} Published Successfully!")
    return redirect(url_for("kb_list"))

if __name__ == "__main__":
    app.run(debug=True)
    

# if uploaded_file.filename.lower().endswith(".doc") or uploaded_file.filename.lower().endswith(".docx"):
#     converter.convert_doc_to_html(input_path, output_path)

# elif uploaded_file.filename.lower().endswith(".pdf"):
#     converter.convert_pdf_to_html(input_path, output_path)

# else:
#     return jsonify({"error": "Unsupported file format"}), 400
from flask import Flask, request, send_file, render_template
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate-pdf", methods=["POST"])
def generate_pdf():
    data = request.json
    name = data["name"]
    address = data["address"]
    rows = data["rows"]
    columns = data["columns"]

    page_width, page_height = A4
    margin = 1 * mm
    spacing = 1 * mm

    label_width = (page_width - 2 * margin - (columns - 1) * spacing) / columns
    label_height = (page_height - 2 * margin - (rows - 1) * spacing) / rows

    pdf_buffer = BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=A4)
    y_start = page_height - margin - label_height

    for row in range(rows):
        for col in range(columns):
            x = margin + col * (label_width + spacing)
            y = y_start - row * (label_height + spacing)
            c.rect(x, y, label_width, label_height)
            text_x = x + 5 * mm
            text_y = y + label_height - 10 * mm
            c.setFont("Helvetica", 10)
            c.drawString(text_x, text_y, name)
            c.drawString(text_x, text_y - 12, address)

    c.save()
    pdf_buffer.seek(0)
    return send_file(pdf_buffer, mimetype="application/pdf", as_attachment=True, download_name="labels.pdf")

if __name__ == "__main__":
    app.run(debug=True)


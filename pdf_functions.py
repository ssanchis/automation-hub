# pdf_report.py
from fpdf import FPDF

class PDFReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Análisis Exploratorio de Datos", ln=True, align="C")

    def chapter_title(self, title):
        self.set_font("Arial", "B", 12)
        self.ln(10)
        self.cell(0, 10, title, ln=True)

    def chapter_body(self, text):
        self.set_font("Arial", "", 10)
        self.multi_cell(0, 10, text)
        self.ln()

    def add_image(self, image_path, w=150):
        self.image(image_path, w=w)
        self.ln()
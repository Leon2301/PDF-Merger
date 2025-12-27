from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import io
import tkinter as tk
from tkinter import filedialog

def create_numbered_overlay(page_number, width, height):
    """Erzeugt eine Seitennummer als Overlay."""
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=(width, height))
    can.setFont("Helvetica", 12)
    can.drawString(width/2, 20, f"Seite {page_number}")
    can.save()
    packet.seek(0)
    return PdfReader(packet).pages[0]

def create_grid_page(width, height, spacing=14):
    """Erzeugt eine karierte Seite (Grid)."""
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=(width, height))

    # horizontale Linien
    y = 0
    while y < height:
        can.setStrokeColorRGB(0.7, 0.7, 0.7)  # hellgrau
        can.line(0, y, width, y)
        y += spacing

    # vertikale Linien
    x = 0
    while x < width:
        can.setStrokeColorRGB(0.7, 0.7, 0.7)
        can.line(x, 0, x, height)
        x += spacing

    can.save()
    packet.seek(0)
    return PdfReader(packet).pages[0]

def merge_pdfs_with_grid_pages():
    root = tk.Tk()
    root.withdraw()
    pdf_files = filedialog.askopenfilenames(
        title="Wähle die PDF-Dateien aus (in Reihenfolge)",
        filetypes=[("PDF Dateien", "*.pdf")]
    )

    if not pdf_files:
        print("Keine Dateien ausgewählt.")
        return

    writer = PdfWriter()
    current_page_number = 1

    for file in pdf_files:
        reader = PdfReader(file)

        for page in reader.pages:
            # Seitennummer Overlay
            overlay = create_numbered_overlay(current_page_number, page.mediabox.width, page.mediabox.height)
            page.merge_page(overlay)
            writer.add_page(page)
            current_page_number += 1

            # Prüfen, ob Text vorhanden
            text = page.extract_text()
            if text and text.strip():
                # 3 karierte Seiten einfügen
                for _ in range(3):
                    grid_page = create_grid_page(page.mediabox.width, page.mediabox.height)
                    overlay_grid = create_numbered_overlay(current_page_number, page.mediabox.width, page.mediabox.height)
                    grid_page.merge_page(overlay_grid)
                    writer.add_page(grid_page)
                    current_page_number += 1

    # Speichern
    save_path = filedialog.asksaveasfilename(
        title="Speichern unter",
        defaultextension=".pdf",
        filetypes=[("PDF Dateien", "*.pdf")]
    )

    if save_path:
        with open(save_path, "wb") as f:
            writer.write(f)
        print(f"PDF gespeichert als: {save_path}")
    else:
        print("Speichern abgebrochen.")

if __name__ == "__main__":
    merge_pdfs_with_grid_pages()

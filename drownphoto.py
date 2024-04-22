from fpdf import FPDF, Align
from wand.image import Image


from pdf2image import convert_from_path

pdf = FPDF()
pdf.core_fonts_encoding ='cp1252'
pdf.set_auto_page_break = False
pdf.add_page()
pdf.ln(30)
pdf.image("vlntn.png" , Align.C, 20, 100) #x=Align.C)



def body(txt):
    pdf.add_font("Arial", style="", fname="Arial Cyr Regular.ttf")
    pdf.set_font("Arial", size=10)
    new_text = ""
    with open(txt, "r", encoding="UTF-8") as fh:
        
        lines = fh.readlines()
        for line in lines:
            new_text += (line)

    # for line in txt:
    #     new_text += line.strip() + " "
    
    
    pdf.multi_cell(40, 5, new_text, center=True)
    pdf.ln()

body("val.txt")
pdf.output("tuto1.pdf")

# Path to the PDF file
pdf_path = "tuto1.pdf"

with Image(filename=pdf_path, resolution=300) as img:
    img.compression_quality = 100
    img.trim()
    img.save(filename="output.jpg")
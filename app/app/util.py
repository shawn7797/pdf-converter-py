from pdf2docx import Converter, parse

def pdfToDocx(pdf_file):
    # pdf_file = 'demo.pdf'
    length = len(pdf_file.split("."))
    doc_file = 'converted/' + pdf_file.split(".")[length-1] + '.docx'

    cv = Converter(pdf_file)
    cv.convert(doc_file, start=0, end=None)

    cv.close()

    return parse(pdf_file, doc_file, start=0, end=None)
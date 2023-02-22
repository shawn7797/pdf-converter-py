from dataclasses import dataclass
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import FileResponse

import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings

from pdf2docx import Converter, parse

def pdfToDocx(pdf_file, name):
    doc_file = 'converted/' + name + '.docx'

    cv = Converter(pdf_file)
    cv.convert(doc_file)

    cv.close()

    parse(pdf_file, doc_file)

    return doc_file
    
@api_view(['POST'])
def convert_pdf_to_docx(request):
    delete_folders()

    pdf_file = request.FILES["file"]

    os.mkdir("converted")
    path = default_storage.save('uploaded/' + pdf_file.name, ContentFile(pdf_file.read()))
    tmp_file = os.path.join(settings.MEDIA_ROOT, path)

    doc_file_name = pdfToDocx(tmp_file, pdf_file.name.split(".pdf")[0])

    return send_file(doc_file_name)

def send_file(file):

    doc = open(file, 'rb')

    response = FileResponse(doc)

    return response

def delete_folders():
    import shutil
    if os.path.isdir('uploaded'):
        shutil.rmtree('uploaded')
        
    if os.path.isdir('converted'):
        shutil.rmtree('converted')

def home(request):
    message = "PDF to DOCX converter on vercel"
    return HttpResponse(message)
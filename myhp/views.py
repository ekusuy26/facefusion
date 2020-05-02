from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import DocumentForm
from .models import Document
from PIL import Image
from django.conf import settings
import cv2
 
def index(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('myhp:index')
    else:
        form = DocumentForm()
        max_id = Document.objects.latest('id').id
        obj = Document.objects.get(id = max_id)
        input_path = settings.BASE_DIR + obj.photo.url
        output_path = settings.BASE_DIR + "/media/mosaics/output.jpg"
        gray(input_path,output_path)
 
    return render(request, 'index.html', {
        'form': form,
        'obj': obj
    })

def gray(input_path,output_path):
    src = cv2.imread(input_path)
    def mosaic(src, ratio=0.1):
        small = cv2.resize(src, None, fx=ratio, fy=ratio, interpolation=cv2.INTER_NEAREST)
        return cv2.resize(small, src.shape[:2][::-1], interpolation=cv2.INTER_NEAREST)
    dst_01 = mosaic(src)
    cv2.imwrite(output_path, dst_01)

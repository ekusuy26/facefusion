from django.shortcuts import render, redirect
from .forms import DocumentForm
from .models import Document
from PIL import Image, ImageFilter
import cv2
 
 
def index(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            img_moto =Image.open(request.FILES['photo'].name)
            src = cv2.imread(img_moto)
            def mosaic(src, ratio=0.1):
                small = cv2.resize(src, None, fx=ratio, fy=ratio, interpolation=cv2.INTER_NEAREST)
                return cv2.resize(small, src.shape[:2][::-1], interpolation=cv2.INTER_NEAREST)
            
            dst_01 = mosaic(src)
            cv2.imwrite('./media/documents/opencv_mosaic_01.jpg', dst_01)

            form.save()
            return redirect('myhp:index')
    else:
        form = DocumentForm()
        obj = Document.objects.all()
 
    return render(request, 'index.html', {
        'form': form,
        'obj': obj
    })

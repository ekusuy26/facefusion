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
            return redirect('model_form_upload/')
    else:
        form = DocumentForm()
        max_id = Document.objects.latest('id').id
        obj = Document.objects.get(id = max_id)
        input_path = settings.BASE_DIR + obj.photo.url
        input_path_two = settings.BASE_DIR + obj.photo_two.url
        output_path = settings.BASE_DIR + "/media/mosaics/output.jpg"
        output_path_two = settings.BASE_DIR + "/media/mosaics/output_two.jpg"
        swap_faces(input_path,input_path_two,output_path,output_path_two)
 
    return render(request, 'myhp/index.html', {
        'form': form,
        'obj': obj
    })

def swap_faces(input_path,input_path_two,output_path,output_path_two):
    src = cv2.imread(input_path)
    src_two = cv2.imread(input_path_two)

    def mosaic(src, ratio=1):
        small = cv2.resize(src, None, fx=ratio, fy=ratio, interpolation=cv2.INTER_NEAREST)
        return cv2.resize(small, src.shape[:2][::-1], interpolation=cv2.INTER_NEAREST)

    def mosaic_area(src, src_two, x, y, width, height, ratio=1):
        dst = src.copy()
        dst_02 = src_two.copy()
        dst[y:y + height, x:x + width] = mosaic(dst_02[y:y + height, x:x + width], ratio)
        return dst

    face_cascade_path = './haarcascade_frontalface_default.xml'
    face_cascade = cv2.CascadeClassifier(face_cascade_path)
    
    src_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    src_two_gray = cv2.cvtColor(src_two, cv2.COLOR_BGR2GRAY)
    
    faces = face_cascade.detectMultiScale(src_gray)
    faces_two = face_cascade.detectMultiScale(src_two_gray)
    
    for x, y, w, h in faces:
        for a, b, c, d in faces_two:
            dst_face_01 = mosaic_area(src, src_two, x, y, w, h)
            dst_face_02 = mosaic_area(src_two, src, a, b, c, d)
        
            cv2.imwrite(output_path, dst_face_01)
            cv2.imwrite(output_path_two, dst_face_02)

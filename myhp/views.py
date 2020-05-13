import cv2
import boto3
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import DocumentForm
from .models import Document
from PIL import Image
from django.conf import settings

s3 = boto3.resource('s3')
bucket = s3.Bucket('facefusion20200510')

def index(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            print('documents is_valid')
            form.save()
        else:
            print('documents false is_valid')
        max_id = Document.objects.latest('id').id
        obj = Document.objects.get(id = max_id)
        obj.out_put = "mosaics/output" + str(max_id) + ".jpg"
        obj.out_put_two = "mosaics/output_two" + str(max_id) + ".jpg"
        obj.save()
        bucket.download_file('media/'+obj.photo.name, 'download1.jpg')
        bucket.download_file('media/'+obj.photo_two.name, 'download2.jpg')
        input_path = settings.BASE_DIR + obj.photo.url
        input_path_two = settings.BASE_DIR + obj.photo_two.url
        output_path = settings.BASE_DIR + "/media/mosaics/output" + str(max_id) + ".jpg"
        output_path_two = settings.BASE_DIR + "/media/mosaics/output_two" + str(max_id) + ".jpg"
        src = cv2.imread('./download1.jpg')
        src_two = cv2.imread('./download2.jpg')
        img = src.copy()
        img_two = src_two.copy()
        def mosaic_area(src, src_two, x, y, width, height, ratio=1):
            dst = src.copy()
            dst_02 = src_two.copy()
            dst[y:y + height, x:x + width] = dst_02[y:y + height, x:x + width]
            return dst
    
        face_cascade_path = './haarcascade_frontalcatface.xml'
        face_cascade = cv2.CascadeClassifier(face_cascade_path)
        face_cascade_two = cv2.CascadeClassifier(face_cascade_path)
        src_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        src_two_gray = cv2.cvtColor(src_two, cv2.COLOR_BGR2GRAY)
        img_two_gray = cv2.cvtColor(img_two, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(src_gray)
        faces_two = face_cascade_two.detectMultiScale(img_two_gray)
        for x, y, w, h in faces:
            for a, b, c, d in faces_two:
                dst_face_01 = mosaic_area(src, src_two, x, y, w, h)
                dst_face_02 = mosaic_area(img_two, img, a, b, c, d)
        
                cv2.imwrite('./download1.jpg', dst_face_01)
                cv2.imwrite('./download2.jpg', dst_face_02)
                bucket.upload_file('download2.jpg', 'media/'+obj.out_put.name')
                bucket.upload_file('download2.jpg', 'media/'+obj.out_put_two.name')
        return redirect('upload/')
    else:
        # s3 = boto3.resource('s3')
        
        # bucket = s3.Bucket('facefusion20200510')
        # bucket.download_file('media/documents/16386660144.jpg', '16386660144.jpg')
        # bucket.upload_file('16386660144.jpg', 'media/tests/16386660144.jpg')
        form = DocumentForm()
    return render(request, 'myhp/index.html', {
        'form': form,
        # 'image': image,
    })

def show(request):
    form = DocumentForm()
    max_id = Document.objects.latest('id').id
    obj = Document.objects.get(id = max_id)
    return render(request, 'myhp/show.html', {
        'form': form,
        'obj': obj
    })
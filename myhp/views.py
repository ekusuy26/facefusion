from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import DocumentForm
from .models import Document
from accounts.models import Dog
from PIL import Image
from django.conf import settings
import cv2
import boto3

s3 = boto3.resource('s3')
bucket = s3.Bucket('facefusion20200510')

def toppage(request):
    dogs = Dog.objects.order_by('-id')
    objs = dogs[:5]
    dog = Dog.objects.filter(user_id=request.user.id)
    if dog.count() == 0:
        dog_flg = 0
    else:
        dog_flg = 1
    headLine = 'ユーザー一覧'
    return render(request, 'myhp/index.html', {
        'dogs': dogs,
        'objs': objs,
        'dog_flg': dog_flg,
        'headLine': headLine,
    })

def index(request, pk):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            print('documents is_valid')
            form.save()
        else:
            print('documents false is_valid')
        faceFusion()
        return redirect('upload/')
    else:
        form = DocumentForm()
        dog = Dog.objects.get(id = pk)
    return render(request, 'myhp/synthesis.html', {
        'form': form,
        'dog': dog,
    })

def show(request):
    form = DocumentForm()
    max_id = Document.objects.latest('id').id
    obj = Document.objects.get(id = max_id)
    return render(request, 'myhp/show.html', {
        'form': form,
        'obj': obj
    })

def result(request):
    objs = Document.objects.all()
    return render(request, 'myhp/result.html', {
        'objs': objs
    })

def faceFusion():
    max_id = Document.objects.latest('id').id
    obj = Document.objects.get(id = max_id)
    obj.out_put = "uploads/output" + str(max_id) + ".jpg"
    obj.out_put_two = "uploads/output_two" + str(max_id) + ".jpg"
    obj.save()
    try:
        bucket.download_file('media/'+obj.photo.name, 'download1.jpg')
        bucket.download_file('media/'+obj.photo_two.name, 'download2.jpg')
        src = cv2.imread('./download1.jpg')
        src_two = cv2.imread('./download2.jpg')
        test = 0
    except:
        input_path = settings.BASE_DIR + obj.photo.url
        input_path_two = settings.BASE_DIR + obj.photo_two.url
        output_path = settings.BASE_DIR + "/media/uploads/output" + str(max_id) + ".jpg"
        output_path_two = settings.BASE_DIR + "/media/uploads/output_two" + str(max_id) + ".jpg"
        src = cv2.imread(input_path)
        src_two = cv2.imread(input_path_two)
        test = 1
    img = src.copy()
    img_two = src_two.copy()
    def face_swap(src, src_two, x, y, width, height, ratio=1):
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
            dst_face_01 = face_swap(src, src_two, x, y, w, h)
            dst_face_02 = face_swap(img_two, img, a, b, c, d)
    
            if test == 0:
                cv2.imwrite('./download1.jpg', dst_face_01)
                cv2.imwrite('./download2.jpg', dst_face_02)
                bucket.upload_file('download1.jpg', 'media/'+obj.out_put.name, ExtraArgs={'ACL':'public-read'})
                bucket.upload_file('download2.jpg', 'media/'+obj.out_put_two.name, ExtraArgs={'ACL':'public-read'})
            else:
                cv2.imwrite(output_path, dst_face_01)
                cv2.imwrite(output_path_two, dst_face_02)
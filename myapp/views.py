from django.shortcuts import render,redirect
from .forms import ImageForm
from .models import Imagemodel
from django.contrib import messages

import keras
from PIL import Image
import numpy as np
import os
from django.core.files.storage import FileSystemStorage

media='meadia'
model=keras.models.load_model('mymodel.h5')

def makepredictions(path):
    img=Image.open(path)
    img_d=img.resize((224,224))

    if len(np.array(img_d).shape) <4 :
        rgb_img=Image.new("RGB",img_d.size)
        rgb_img.paste(img_d)
    else:
        rgb_img=img_d
    #convert img to numpy array & reshape
    rgb_img=np.array(rgb_img,dtype=np.float64)
    rgb_img=rgb_img.reshape(1,224,224,3)

    #makepredictions
    predictions=model.predict(rgb_img)
    n=int(np.argmax(predictions))
    if n==1:
        n="Result:C1 level"
    elif n==2:
        n="Result:C2 level"
    else:
        n="Result:C3 level"
    return n

# Create your views here.
def home(request):
    return render(request,'myapp/base.html')

def upload(request):          #Training model
    form=ImageForm(request.POST,request.FILES)
    if form.is_valid():
        form.save()
    messages.success(request,"Image uploaded successfully!!")
    form=ImageForm()
    img1=Imagemodel.objects.all()
    # img2=Imagemodel.objects.get(photo=form['photo'])
    # path = img1.photo.url
    # print(img2)

     # predictions=makepredictions(path)
    return render(request, 'myapp/bs.html',{'img':img1,'form':form})


# def cnnpredict(request,id):
#     im=Imagemodel.objects.filter(id=id)
#     p=im.photo.path
#     predictions=makepredictions(p)
#     return redirect('/upload',{'im':im,'predict':predictions})

def delete_img(request,id):
    im=Imagemodel.objects.filter(id=id)
    # if len(im.photo.path)>0:
    #     os.remove(im.photo.path)
    im.delete()
    return redirect('/upload')



def test(request):
    form=ImageForm(request.POST,request.FILES)
    if form.is_valid():
        form.save()
    form=ImageForm()
    img=Imagemodel.objects.all()
    return render(request, 'myapp/test.html',{'img':img,'form':form})
# def test(request):
#     if request.method=="POST" and request.FILES['uploaded']:
#         if 'upload' not in request.FILES:
#            err="No images selected"
#            return render(request,'index.html',{'err':err})
#         f=request.FILES['uploaded']
#         if f=="":
#             err="No files selected"
#             return render(request,'index.html',{'err':err})
#         uploaded=request.FILES['uploaded']
#         fss=FileSystemStorage()
#         file=fss.save(uploaded.name,upload)
#         file_url=fss.url(file)
#         predictions=makepredictions(os.path.join(media,file))
#         return render(request,'test.html',{'pred':predictions,'file_url':file_url})

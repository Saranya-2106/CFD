from django.http import HttpResponse
from django.shortcuts import render
from PIL import Image
from pytesseract import pytesseract
import cv2
import pytesseract
from .models import *
from skimage import io
from io import BytesIO
from PIL import Image
import urllib.request
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
 
# Opens a image in RGB mode
# im = Image.open(r"C:\Users\HP\Desktop\cheque\filled2.png")
 

 
# Setting the points for cropped image
def get_date(im2):
    urllib.request.urlretrieve(im2, "img")
    im = Image.open("img")
    width, height = im.size
    left = 2*width/3    
    top = 0
    right = width
    bottom = height/5;
    im1 = im.crop((left, top, right, bottom))
    buffer = BytesIO()
    im1.save(fp=buffer, format='JPEG')
    return ContentFile(buffer.getvalue())
   

def get_name(im2):
    urllib.request.urlretrieve(im2, "img")
    im = Image.open("img")
    width, height = im.size
    left = height/8
    top = 2*height/8
    right = width*3/4
    bottom = 2.7*height/8
    im1 = im.crop((left, top, right, bottom))
    buffer = BytesIO()
    im1.save(fp=buffer, format='JPEG')
    return ContentFile(buffer.getvalue())


    
def amount_in_words(im2):
    urllib.request.urlretrieve(im2, "img")
    im = Image.open("img")
    width, height = im.size
    left = height/5
    top = 2.5*height/8
    right = width*0.70
    bottom = 4*height/8
    im1 = im.crop((left, top, right, bottom))
    buffer = BytesIO()
    im1.save(fp=buffer, format='JPEG')
    return ContentFile(buffer.getvalue())

        
def amount_in_number(im2):
    urllib.request.urlretrieve(im2, "img")
    im = Image.open("img")
    width, height = im.size
    left = 2.3*width/3
    top = 3.5*height/8
    right = 9.67*width/10
    bottom = 4.5*height/8
    im1 = im.crop((left, top, right, bottom))
    buffer = BytesIO()
    im1.save(fp=buffer, format='JPEG')
    return ContentFile(buffer.getvalue())

   
def get_signature(im2):
    urllib.request.urlretrieve(im2, "img")
    im = Image.open("img")
    width, height = im.size
    left = 2*width/3
    top = 3*height/4
    right = width
    bottom = height
    im1 = im.crop((left, top, right, bottom))
    buffer = BytesIO()
    im1.save(fp=buffer, format='JPEG')
    return ContentFile(buffer.getvalue())

def get_acc(im2):
    urllib.request.urlretrieve(im2, "img")
    im = Image.open("img")
    width, height = im.size
    left=width/8
    right=width/3.5
    top=4*(height/7)
    bottom=4.70*(height/7)
    im1 = im.crop((left, top, right, bottom))
    buffer = BytesIO()
    im1.save(fp=buffer, format='JPEG')
    return ContentFile(buffer.getvalue())

def imageTotext(image):
    image = io.imread(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3,3), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Morph open to remove noise and invert image
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    invert = 255 - opening

    # Perform text extraction
    data = pytesseract.image_to_string(invert, lang='eng', config='--psm 6')
    return data

def index(request):
    context = {}
    if request.POST:
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        cheque = Cheque.objects.create()
        cheque.chequeImage = request.FILES['file']
        cheque.save()
        image = "http://localhost:8000"+cheque.chequeImage.url
        date = cheque.dateImage
        image_name = "date"+str(cheque.id)+".jpg"
        img = get_date(image)
        date.save(image_name, InMemoryUploadedFile(
            img,None,image_name,'image/jpeg',img.tell,None
        ))

        name = cheque.nameImage
        image_name = "name"+str(cheque.id)+".jpg" 
        img = get_name(image)
        name.save(image_name, InMemoryUploadedFile(
            img,None,image_name,'image/jpeg',img.tell,None
        ))

        amountwords = cheque.amountWordsImage
        image_name = "amountwords"+str(cheque.id)+".jpg"
        img = amount_in_words(image)
        amountwords.save(image_name, InMemoryUploadedFile(
            img,None,image_name,'image/jpeg',img.tell,None
        ))

        amount = cheque.amountImage
        image_name = "amount"+str(cheque.id)+".jpg"
        img = amount_in_number(image)
        amount.save(image_name, InMemoryUploadedFile(
            img,None,image_name,'image/jpeg',img.tell,None
        ))

        signature = cheque.signatureImage
        image_name = "signature"+str(cheque.id)+".jpg"
        img = get_signature(image)
        signature.save(image_name, InMemoryUploadedFile(
            img,None,image_name,'image/jpeg',img.tell,None
        ))

        accno = cheque.accnoImage
        image_name = "accno"+str(cheque.id)+".jpg"
        img = get_acc(image)
        accno.save(image_name, InMemoryUploadedFile(
            img,None,image_name,'image/jpeg',img.tell,None
        ))

        name = imageTotext("http://localhost:8000"+cheque.nameImage.url)
        date = imageTotext("http://localhost:8000"+cheque.dateImage.url)
        amountInWords = imageTotext("http://localhost:8000"+cheque.amountWordsImage.url)
        amount = imageTotext("http://localhost:8000"+cheque.amountImage.url)
        accNo = imageTotext("http://localhost:8000"+cheque.accnoImage.url)
    
        userBankInfoObj = UserbankInfo.objects.get(accNo = accNo)
        context = {"userBankInfo":userBankInfoObj,"cheque":cheque}
    return render(request,'core/index.html',context)
    
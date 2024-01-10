from django.db import models
from PIL import Image


class UserbankInfo(models.Model):
    accNo = models.CharField(max_length = 20,null=True,blank=True)
    accHolderName = models.CharField(max_length = 20,null=True,blank=True)
    signature = models.ImageField(null=True,blank=True)
    phoneNumber = models.PositiveBigIntegerField(null=True,blank=True)
    balance = models.PositiveIntegerField(null=True,blank=True)
    image = models.ImageField(upload_to="profile_pic/",null=True,blank=True)

class Cheque(models.Model):
    chequeImage = models.ImageField(upload_to="cheque/", null=True,blank=True)
    dateImage = models.ImageField(upload_to="date/", null=True,blank=True)
    amountWordsImage = models.ImageField(upload_to="amountWords/", null=True,blank=True)
    amountImage = models.ImageField(upload_to="amount/", null=True,blank=True)
    nameImage = models.ImageField(upload_to="name/", null=True,blank=True)
    signatureImage = models.ImageField(upload_to="signature/", null=True,blank=True)
    accnoImage = models.ImageField(upload_to="accno/",null=True,blank=True)
    date = models.DateField(null=True,blank=True)
    chequeNo = models.PositiveIntegerField(null=True,blank=True)
    micrCode = models.PositiveIntegerField(null=True,blank=True)
    rbiAccNo = models.PositiveIntegerField(null=True,blank=True)
    transactionCode = models.PositiveIntegerField(null=True,blank=True)
    accHolder = models.ForeignKey(UserbankInfo,null=True,blank=True,on_delete=models.CASCADE)

    # def save(self):
    #     super().save()

    #     img = Image.open(self.image.path)
    #     if img.height >300 or img.width >300:
    #         oputput_size = (300,300)
    #         img.thumbnail(oputput_size)
    #         img.save(self.image.path)

class Transaction(models.Model):
    STATUS_CHOICES = (
        ("Success","Success"),
        ("Failed","Failed"),
        ("Bounced","Bounced"),
    )
    cheque = models.ForeignKey(Cheque,null=True,blank=True,on_delete=models.CASCADE)
    accNo = models.ForeignKey(UserbankInfo,null=True,blank=True,on_delete=models.CASCADE)
    receiver = models.CharField(max_length = 20,null=True,blank=True)
    status = models.CharField(max_length = 20,choices=STATUS_CHOICES,null=True,blank=True)
    amount = models.PositiveIntegerField(null=True,blank=True)
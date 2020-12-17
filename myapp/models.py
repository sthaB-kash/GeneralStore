from django.db import models
from django.db import connections

import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
# Create your models here.
from rest_framework import serializers


class Supplier(models.Model):
    sname = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    contact = models.CharField(max_length=10)
    email = models.EmailField(max_length=50)

    class Meta:
        db_table = "supplier"

    def __str__(self):
        return self.sname


class Product(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    pid = models.CharField(max_length=50, default='')
    pname = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    price = models.FloatField()
    qty = models.IntegerField()
    total_price = models.FloatField()
    doe = models.DateTimeField(auto_now_add=True)
    mfd = models.DateField()
    exp = models.DateField()
    qr_code = models.ImageField(upload_to='qr_codes')

    def __str__(self):
        return self.pname

    class Meta:
        db_table = "Product"

    def save(self, *args, **kwargs):
        qrcode_img = qrcode.make(self.pname)
        canvas = Image.new('RGB', (290, 290), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.pname}.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)


class Billing(models.Model):
    cname = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    purchase_items = models.JSONField()
    total_price = models.DecimalField(max_digits=5, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        db_table = "billing"

    def __str__(self):
        return self.cname


class Students(models.Model):
    sid = models.IntegerField()
    name = models.CharField(max_length=50)
    semester = models.IntegerField()
    program = models.CharField(max_length=30)

    class Meta:
        db_table = "students"

    def __str__(self):
        return self.name


from django.contrib import admin
from . models import Imagemodel
# Register your models here.

@admin.register(Imagemodel)
class ImageAdmin(admin.ModelAdmin):
    list_display=['id','photo','date']

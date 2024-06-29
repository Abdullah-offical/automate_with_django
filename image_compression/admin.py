from django.contrib import admin
from .models import CompressImage
from django.utils.html import format_html

class CompressImageAdmin(admin.ModelAdmin):
    def thumbnail(self, obj):
        return format_html(f'<img src="{obj.compressed_img.url}" width="40" height="40">')
    list_display = ('user', 'thumbnail')
    
admin.site.register(CompressImage, CompressImageAdmin)

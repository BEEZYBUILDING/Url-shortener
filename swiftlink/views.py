from django.shortcuts import render, redirect, get_object_or_404
from .models import Url
import hashlib

# Create your views here.
def shortener(request, url):
    
    alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-_"
    is_unique = False
    salt = ''
    while not is_unique:
        temp = url+salt
        encoded = temp.encode('utf-8')
        encoder = hashlib.md5()
        encoder.update(encoded)
        hexed_string = encoder.hexdigest()
        hex_digit = hexed_string[:8]
        new_hex = int(hex_digit, 16)
        short_key = ''
        while len(short_key) <6: 
            remainder = new_hex % 64
            char = str(alphabet[remainder])
            short_key = short_key+char
            new_hex = new_hex // 64
            
        if Url.objects.filter(short_key=short_key).exists():
            salt += 'a'
        else:
            is_unique=True
    new_object = Url.objects.create(original_url= url, short_key=short_key )
    return render(request,'swiftlink/base.html', {'new_url': new_object})
        
        
def redirect_url(request, short_key):
    link = get_object_or_404(Url, short_key=short_key)
    return redirect(link.original_url)
    
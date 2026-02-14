from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm
from .models import Url
import hashlib

# Create your views here.
def home(request):
    return render(request, 'swiftlink/base.html')

@login_required
def dashboard(request):
    new_url = None
    if request.method == 'POST':
        alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-_"
        original_url = request.POST.get('original_url')
        is_unique = False
        if not original_url.url.startswith(('http://', 'https://')):
            url = 'https://' + url
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
        new_url = Url.objects.create(original_url= original_url, short_key=short_key, user=request.user )
    urls = Url.objects.filter(user=request.user).order_by('-created')
    return render(request,'swiftlink/dashboard.html', {'urls': urls, 'new_url': new_url})
            
            
def redirect_url(request, short_key):
    link = get_object_or_404(Url, short_key=short_key)
    return redirect(link.original_url)

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()
            auth_login(request, user)
            return redirect('swiftlink:login')
    else:
        form = RegisterForm()
    return render(request, 'swiftlink/register.html', {'form': form})

def delete_url(request, short_key):
    url = get_object_or_404(Url, short_key=short_key, user=request.user)
    if request.method == 'POST':
        url.delete()
        return redirect('swiftlink:dashboard')

"""def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username= cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    return HttpResponse('Authenticated Sucessfully')
                else:
                    return HttpResponse('Account has been disabled')
            else:
                return HttpResponse('Invalid login')
    else:
        form =LoginForm()
    return render(request, 'swiftlink/login.html', {'form': form})"""
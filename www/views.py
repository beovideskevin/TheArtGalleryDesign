from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import escape, strip_tags
from www.models import Category, Artwork
from www.helpers import *
import logging
logger = logging.getLogger(__name__)

# Create your views here.
def home(request):
    return render(request, "home.html", {
        "keywords": "art portfolio, contemporary painting, colorful illustration, fine art prints, modern artist",
    })

def painting(request):
    category = Category.objects.get(name="painting")
    images = Artwork.objects.filter(category=category).order_by('index')
    return render(request, "gallery.html", {
        "keywords": "contemporary art, original paintings, abstract painting, colorful artwork",
        "images": images,
        "active": "painting",
    })

def illustration(request):
    category = Category.objects.get(name="illustration")
    images = Artwork.objects.filter(category=category).order_by('index')
    return render(request, "gallery.html", {
        "keywords": "illustration portfolio, custom illustration, book illustration, digital illustration",
        "images": images,
        "active": "illustration",
    })

def design(request):
    category = Category.objects.get(name="design")
    images = Artwork.objects.filter(category=category).order_by('index')
    return render(request, "gallery.html", {
        "keywords": "graphic design, creative designer, branding and design",
        "images": images,
        "active": "design",
    })

def photography(request):
    category = Category.objects.get(name="photography")
    images = Artwork.objects.filter(category=category).order_by('index')
    return render(request, "gallery.html", {
        "keywords": "fine art photography, creative photography, photo art prints",
        "images": images,
        "active": "photography",
    })

def installation(request):
    category = Category.objects.get(name="installation")
    images = Artwork.objects.filter(category=category).order_by('index')
    return render(request, "gallery.html", {
        "keywords": "art installations, contemporary installations, site-specific art",
        "images": images,
        "active": "installation",
    })

def recent(request):
    category = Category.objects.get(name="recent")
    images = Artwork.objects.filter(category=category).order_by('index')
    return render(request, "gallery.html", {
        "keywords": "new artworks, latest collection, art updates, recent paintings, creative projects",
        "images": images,
        "active": "recent",
    })

def gallery(request, cat):
    try:
        category = Category.objects.get(name=cat)
    except Category.DoesNotExist:
        logger.error(f"Gallery: category {cat} does not exist.")
        return render(request, "404.html")

    images = Artwork.objects.filter(category=category).order_by('index')
    return render(request, "gallery.html", {
        "keywords": "art portfolio, contemporary painting, colorful illustration, fine art prints, modern artist",
        "images": images,
        "active": "photography",
    })

def about(request):
    return render(request, "about.html", {
        "keywords": "artist portfolio, creative visual artist, contemporary artist",
    })

def contact(request):
    if request.method == "POST":
        secret = settings.TURNSTILE_SECRET
        turnstile_response = request.POST.get("cf-turnstile-response", "")
        remote_ip = request.META.get('HTTP_CF_CONNECTING_IP')
        name = strip_tags(escape(request.POST["name"]))
        email = strip_tags(escape(request.POST["email"]))
        message = strip_tags(escape(request.POST["message"]))
        nothing = strip_tags(escape(request.POST["nothing"]))
        sent = False
        error = False

        if (name == "" or message == "" or email == "" or is_valid_email(email) is False or nothing != "" 
                or turnstile_response == '' or validate_turnstile(secret, turnstile_response, remote_ip) is False):
            error = True
            url = reverse('contact') + f"?name={name}&email={email}&message={message}&error={error}&sent={sent}"
            return redirect(url)

        send_mail(
            "Mensaje de TheArtGalleryDesign.com",
            f"{message}\nNombre: {name}\nCorreo: {email}",
            settings.EMAIL_HOST_USER,
            [settings.ADMIN_USER_EMAIL],
            fail_silently=True,
        )
        sent = True
        url = reverse('contact') + f"?sent={sent}"
        return redirect(url)

    name = request.GET.get('name', "") 
    message = request.GET.get('message', "")
    email = request.GET.get('email', "")
    sent = request.GET.get('sent', False)
    error = request.GET.get('error', False)

    return render(request, "contact.html", {
        "keywords": "art portfolio, contemporary painting, colorful illustration, fine art prints, modern artist",
        "error": error,
        "name": name,
        "email": email,
        "message": message,
        "sent": sent
    })
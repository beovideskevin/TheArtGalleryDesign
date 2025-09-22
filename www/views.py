from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import escape, strip_tags
from www.models import Category, Artwork
from www.helpers import *
import logging
logger = logging.getLogger(__name__)

# Create your views here.
def home(request):
    return render(request, "home.html", {})

def painting(request):
    category = Category.objects.get(name="painting")
    images = Artwork.objects.filter(category=category).order_by('index')
    return render(request, "gallery.html", {
        "images": images,
        "active": "painting",
    })

def illustration(request):
    category = Category.objects.get(name="illustration")
    images = Artwork.objects.filter(category=category).order_by('index')
    return render(request, "gallery.html", {
        "images": images,
        "active": "illustration",
    })

def design(request):
    category = Category.objects.get(name="design")
    images = Artwork.objects.filter(category=category).order_by('index')
    return render(request, "gallery.html", {
        "images": images,
        "active": "design",
    })

def photography(request):
    category = Category.objects.get(name="photography")
    images = Artwork.objects.filter(category=category).order_by('index')
    return render(request, "gallery.html", {
        "images": images,
        "active": "photography",
    })

def installation(request):
    category = Category.objects.get(name="installation")
    images = Artwork.objects.filter(category=category).order_by('index')
    return render(request, "gallery.html", {
        "images": images,
        "active": "installation",
    })

def recent(request):
    category = Category.objects.get(name="recent")
    images = Artwork.objects.filter(category=category).order_by('index')
    return render(request, "gallery.html", {
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
        "images": images,
        "active": "photography",
    })

def about(request):
    return render(request, "about.html", {})

def contact(request):
    sent = False
    if request.method == "POST":
        secret = settings.TURNSTILE_SECRET
        turnstile_response = request.POST.get("cf-turnstile-response", "")
        remote_ip = request.META.get('HTTP_CF_CONNECTING_IP')
        name = request.POST["name"]
        email = request.POST["email"]
        message = request.POST["message"]
        nothing = request.POST["nothing"]

        if (name == "" or email == "" or is_valid_email(email) is False or message == ""
                or turnstile_response == '' or nothing != ""):
            return render(request, "contact.html", {
                "error": True,
                "name": name,
                "email": email,
                "message": message
            })

        if validate_turnstile(secret, turnstile_response, remote_ip) is False:
            return render(request, "contact.html", {
                "error": True,
                "name": name,
                "email": email,
                "message": message
            })

        name = strip_tags(escape(name))
        message = strip_tags(escape(message))
        email = strip_tags(escape(email))

        sent = True
        send_mail(
            "Mensaje de TheArtGalleryDesign.com",
            f"{message}\nNombre: {name}\nCorreo: {email}",
            settings.EMAIL_HOST_USER,
            [settings.ADMIN_USER_EMAIL],
            fail_silently=True,
        )

    return render(request, "contact.html", {
        "sent": sent
    })
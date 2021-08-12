from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as dj_login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.mail import send_mail
from django.conf import settings

from .models import Contact, Post
from .forms import ContactForm, LoginForm, InscriptionForm, CommentForm


def connexion(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    dj_login(request, user)
                    return redirect("index")
                else:
                    messages.warning(
                        request,
                        "Vous êtes déconnecté",
                        "warning"
                    )
            else:
                messages.warning(
                    request,
                    "Vérifiez vos informations de connexion, puis réessayer",
                    "warning"
                )         
    else:
        form = LoginForm()
    ctx = {"form": form}
    return render(request, "blog/login.html", ctx)


def inscription(request):
    if request.method == "POST":
        form = InscriptionForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data["password"])
            new_user.save()
            messages.success(request, "Inscription avec succès", "success")
            return redirect("connexion")
        else:
            messages.warning(request, "Veuillez renseigner tous les champs", "warning")
    else:
        form = InscriptionForm()
    ctx = {"form": form}
    return render(request, "blog/inscription.html", ctx)


def deconnexion(request):
    logout(request)
    messages.info(request, "Déconnexion avec succès", "info")
    return render(request, "blog/deconnexion.html")

@login_required
def index(request):
    return render(request, "blog/index.html")

def post_list(request):
    articles = Post.objects.filter(status=1).order_by("-created_on")
    page = request.GET.get('page', 1)
    paginator = Paginator(articles, 10)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    ctx = {
        "posts": posts,
    }
    return render(request, "blog/post_list.html", ctx)

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)
    new_comment = False
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            # Création de l'objet Comment sans sauvegarde
            new_comment = form.save(commit=False)
            # Assignation du post courant à l'objet comment
            new_comment.post = post
            # Enregistrement dans la base de donnee
            new_comment.save()
        else:
            messages.warning(request, "Veuillez renseigner tous les champs", "warning")
    else:
        form = CommentForm()
    ctx = {
        "post": post,
        "comments": comments,
        "new_comment": new_comment,
        "form": form,
    }
    return render(request, "blog/post_detail.html", ctx)

def apropos(request):
    return render(request, "blog/apropos.html")

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            email = form.cleaned_data.get("email")
            message = form.cleaned_data.get("message")

            # Sauvegarde dans la base de donnee 
            new_contact = Contact(
                name=name,
                email=email,
                message=message
            )
            new_contact.save()

            # Envoi email de confirmation
            subject = "Confirmation reception de votre message"
            body = f"""
                Bonjour {name},
                Nous avons bien reçu votre message, et nous mettons 
                tous en oeuvre pour vous répondre dans les meilleurs delais.
            """
            send_mail(
                subject,
                body,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently = False
            )
        
            # Flash message de confirmation
            messages.success(
                request,
                "Votre message a été envoyé avec succès",
                "success"
            )
            return redirect("contact")
        else:
            messages.warning(
                request, 
                "Veuillez renseigner tous les champs puis réessayer",
                "warning"
            )
    else:
        form = ContactForm()
    ctx = {"form": form}
    return render(request, "blog/contact.html", ctx)


from .decorators import login_required
import bcrypt
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError
from .models import Messages, Comments

@login_required
def index(request):

    context = {
        'saludo': 'Hola'
    }
    return render(request, 'index.html', context)

@login_required
def home(request):
    messages = Messages.objects.all()
    comments = Comments.objects.all()
    context = {
        'messages': messages,
        'comments': comments
    }
    return render(request, '/home.html', context)
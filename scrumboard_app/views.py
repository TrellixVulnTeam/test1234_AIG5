from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import *
from .models import *

# Create your views here.


def index(request):
    if request.user.is_authenticated:  # Redirect se l'utente è loggato
        return redirect('dashboard')
    else:
        return redirect('login')


def dashboard(request):
    if request.user.is_authenticated:
        utenteCorrente = ScrumUser.objects.get(username=request.user.username)
        attrs = []
        listaBoard = Board.objects.filter(utentiAssociati=utenteCorrente)
        for board in listaBoard:
            colonne = board.getColonneBoard()
            numcard = 0
            for colonna in colonne:
                numcard += len(colonna.getCardColonna())
            attrs.append({
                        'nome': board.nome,
                        'numCard': numcard
            })
        return render(request, "scrumboard_app/dashboard.html", {'boards': attrs})
    else:
        return redirect('login')

def loginView(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid() is True:
            un = form.cleaned_data['username']
            pw = form.cleaned_data['password']
            user = authenticate(request, username=un, password=pw)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                # TODO: modulo di errore vero
                form.add_error(None, "Errore di autenticazione")
    else:
        form = LoginForm()
    return render(request, "scrumboard_app/login.html", {'form': form})


def logoutView(request):
    logout(request)
    return redirect('index')


def registerView(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid() and form.cleaned_data['password'] == form.cleaned_data['conferma_password'] and not ScrumUser.objects.filter(username = form.cleaned_data['username']).exists():
            user = ScrumUser()
            user.username = form.cleaned_data['username']
            user.set_password(form.cleaned_data['password'])
            user.active = True
            user.staff = False
            user.admin = False
            user.save()
            login(request, user)
            return redirect('index')
        else:
            form.add_error(None, "Errore durante la registrazione utente.")
    else:
        form = RegisterForm()
    return render(request, "scrumboard_app/register.html", {'form': form})



def burndown(request, board_id):
    pass


def board_utente(request, board_id):
    pass

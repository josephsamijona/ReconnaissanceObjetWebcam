# logic/views.py
from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView as DjangoLoginView, LogoutView as DjangoLogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView
from .forms import SignupForm, APIKeyForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class SignupView(View):
    """
    Gère l'inscription des nouveaux utilisateurs.
    """
    form_class = SignupForm
    template_name = 'signup.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')  # Rediriger les utilisateurs déjà authentifiés vers le tableau de bord
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')  # Rediriger les utilisateurs déjà authentifiés vers le tableau de bord
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Connecter l'utilisateur après l'inscription
            messages.success(request, "Inscription réussie. Veuillez vous connecter.")
            return redirect('login')  # Rediriger vers la page de connexion après l'inscription
        return render(request, self.template_name, {'form': form})


class LoginView(DjangoLoginView):
    """
    Gère la connexion des utilisateurs.
    """
    template_name = 'login.html'
    authentication_form = AuthenticationForm

    def get_success_url(self):
        return reverse_lazy('dashboard')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')  # Rediriger les utilisateurs déjà authentifiés vers le tableau de bord
        return super().dispatch(request, *args, **kwargs)
def logout_view(request):
    """
    Logs out the user and redirects to the login page.
    """
    logout(request)  # Déconnecte l'utilisateur
    messages.success(request, "Vous avez été déconnecté avec succès.")  # Message de confirmation
    return redirect('login')  # Redirige vers la page de connexion
class DashboardView(LoginRequiredMixin, View):
    """
    Affiche le tableau de bord principal avec les options pour utiliser la clé par défaut ou la clé utilisateur.
    """
    template_name = 'dashboard.html'
    login_url = 'login'

    def get(self, request):
        return render(request, self.template_name)

class UseDefaultKeyView(View):
    """
    Redirects to the analysis interface.
    """
    def post(self, request):
        return redirect('analyze_interface')

class EnterUserKeyView(View):
    """
    Allows the user to enter their own API key.
    """
    form_class = APIKeyForm
    template_name = 'enter_user_key.html'

    def get(self, request):
        # Pré-remplit le formulaire avec les données existantes de l'utilisateur
        user_profile = UserProfile.objects.get(user=request.user)
        form = self.form_class(instance=user_profile)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        # Récupère le profil utilisateur associé
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        form = self.form_class(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()  # Sauvegarde les changements dans la base de données
            messages.success(request, "Votre clé API a été enregistrée avec succès.")
            return redirect('analyze_interface')  # Redirection vers la vue principale
        return render(request, self.template_name, {'form': form})

@login_required(login_url='login')
def analyze_interface(request):
    """
    View to render the analyze interface with the appropriate API key.
    """
    # Récupération du profil utilisateur associé
    try:
        user_profile = request.user.userprofile
        # Utilisation de la clé API de l'utilisateur si disponible
        api_key = user_profile.huggingface_api_key if user_profile.huggingface_api_key else settings.HUGGINGFACE_API_KEY
    except UserProfile.DoesNotExist:
        # Si aucun profil n'existe pour l'utilisateur, utiliser la clé par défaut
        api_key = settings.HUGGINGFACE_API_KEY

    return render(request, 'analyze_interface.html', {'api_key': api_key})
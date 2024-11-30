# logic/urls.py

from django.urls import path
from .views import (
    SignupView, 
    LoginView, 
    logout_view, 
    DashboardView, 
    UseDefaultKeyView, 
    EnterUserKeyView, 
    analyze_interface,
     
    
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', LoginView.as_view(), name='login'),  # Racine URL pointe vers la page de connexion
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('use-default-key/', UseDefaultKeyView.as_view(), name='use_default_key'),
    path('enter-user-key/', EnterUserKeyView.as_view(), name='enter_user_key'),
    path('analyze-interface/', analyze_interface, name='analyze_interface'),
    #path('api/analyze/', AnalyzeImageView.as_view(), name='analyze_image'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

from django.urls import path
from .views import StudentRegistrationView, CustomLoginView, UserProfileView

urlpatterns = [
    path('register/student/', StudentRegistrationView.as_view(), name='register-student'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
]
from django.urls import path
from .views import StudentRegistrationView, CustomLoginView, UserProfileView,AcademicSupervisorRegistrationView,WorkplaceSupervisorRegistrationView

urlpatterns = [
    path('register/student/', StudentRegistrationView.as_view(), name='register-student'),
    path('register/academic-supervisor/', AcademicSupervisorRegistrationView.as_view(), name='register-supervisor'),
    path('register/workplace/', WorkplaceSupervisorRegistrationView.as_view(), name='register-workplace'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
]
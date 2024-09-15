from django.urls import path
from .views import AddStudentView, GetStudentsView, GetTokenView, VerifyOTPView, SendOTPView

urlpatterns = [
    path('add/', AddStudentView.as_view(), name='add-student'),
    path('get/', GetStudentsView.as_view(), name='get-students'),
    path('token/', GetTokenView.as_view(), name='token_obtain_pair'),
    path('send-otp/', SendOTPView.as_view(), name='send-otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
]

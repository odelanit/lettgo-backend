from django.urls import path

from author.views import CustomAuthToken, CloseAccount, ChangePasswordView

urlpatterns = [
    path('auth/login', CustomAuthToken.as_view()),
    # Author Routes
    path('author/change_password', ChangePasswordView.as_view()),
    path('author/close', CloseAccount.as_view()),
]

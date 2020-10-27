from django.urls import path

from author.views import CustomAuthToken, CloseAccount, ChangePasswordView, ProfileChangeView, UserCreationView, \
    UserActivationView

urlpatterns = [
    path('auth/login', CustomAuthToken.as_view()),
    path('auth/register', UserCreationView.as_view()),
    path('auth/activate/<uid64>/<token>', UserActivationView.as_view()),
    # Author Routes
    path('author/change_password', ChangePasswordView.as_view()),
    path('author/profile', ProfileChangeView.as_view()),
    path('author/close', CloseAccount.as_view()),
]

from django.urls import path

from backend.views import UserList, UserCreate, UserUpdate, CategoryList, CategoryCreate, CategoryUpdate, AreaList, \
    AreaCreate, AreaUpdate, AdvertList, AdvertCreate, AdvertUpdate, CustomAuthToken, ImageUploadView

urlpatterns = [
    path('auth/login', CustomAuthToken.as_view()),

    path('user/list', UserList.as_view()),
    path('user/create', UserCreate.as_view()),
    path('user/<pk>', UserUpdate.as_view()),

    path('category/list', CategoryList.as_view()),
    path('category/create', CategoryCreate.as_view()),
    path('category/<pk>', CategoryUpdate.as_view()),

    path('area/list', AreaList.as_view()),
    path('area/create', AreaCreate.as_view()),
    path('area/<pk>', AreaUpdate.as_view()),

    path('advert/list', AdvertList.as_view()),
    path('advert/create', AdvertCreate.as_view()),
    path('advert/<pk>', AdvertUpdate.as_view()),

    path('image/upload', ImageUploadView.as_view()),
]

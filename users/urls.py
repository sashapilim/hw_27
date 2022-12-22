from django.urls import path

from users.views import UserView, UserDetail, UserCreateView,UserDeleteView,UserUpdateView

urlpatterns = [

    path('user/', UserView.as_view()),
    path('user/<int:pk>/', UserDetail.as_view()),
    path('user/create/', UserCreateView.as_view()),
    path('ad/<int:pk>/update/', UserUpdateView.as_view()),
    path('ad/<int:pk>/delete/', UserDeleteView.as_view()),

]

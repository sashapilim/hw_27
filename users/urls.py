from django.urls import path

from users.views import UserView, UserDetail, UserCreateView, UserDeleteView, UserUpdateView, LocationViewSet
from rest_framework import routers

router=routers.SimpleRouter()
router.register('location', LocationViewSet)
urlpatterns = [

    path('user/', UserView.as_view()),
    path('user/<int:pk>/', UserDetail.as_view()),
    path('user/create/', UserCreateView.as_view()),
    path('user/<int:pk>/update/', UserUpdateView.as_view()),
    path('user/<int:pk>/delete/', UserDeleteView.as_view()),

]
urlpatterns+=router.urls

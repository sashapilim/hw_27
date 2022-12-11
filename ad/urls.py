from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('cat/', views.CategoriesView.as_view(), name="CategoriesView"),
    path('ad/', views.AdsView.as_view(), name='AdsView'),
    path('cat/<int:pk>', views.CategoryViewDetail.as_view(), name='CategoryViewDetail'),
    path('ad/<int:pk>',views.AdsViewDetail .as_view(), name = 'AdsViewDetail')
]

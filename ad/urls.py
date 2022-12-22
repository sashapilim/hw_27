from django.urls import path

from . import views
from .views.ads import AdsView, AdsViewDetail, AdUpadeteView, AdDeleteView, AdUploadImageView
from .views.cat import CategoriesView, CategoryViewDetail, CategoryUpadeteView, CategoryDeleteView

urlpatterns = [


    path('ad/', AdsView.as_view(), name='AdsView'),
    path('ad/<int:pk>', AdsViewDetail.as_view(), name='AdsViewDetail'),
    path('ad/<int:pk>/update', AdUpadeteView.as_view()),
    path('ad/<int:pk>/delete', AdDeleteView.as_view()),
    path('cat/', CategoriesView.as_view(), name="CategoriesView"),
    path('cat/<int:pk>/', CategoryViewDetail.as_view(), name='CategoryViewDetail'),
    path('cat/<int:pk>/update/', CategoryUpadeteView.as_view()),
    path('cat/<int:pk>/delete/', CategoryDeleteView.as_view()),
    path('ad/<int:pk>/upload_image/', AdUploadImageView.as_view())

]

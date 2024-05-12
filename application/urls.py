from django.urls import path

from . import views

app_name = 'application'

urlpatterns = [
    path('', views.index),
    path('index.html', views.index, name='index'),
    path('application/<int:app_id>/', views.application_detail, name='app_detail'),
    path('create/', views.application_create, name='app_create'),
    path('app/<int:app_id>/delete/', views.application_delete, name='app_delete'),
    path('create_deals/', views.bitrix_deals, name='create_deals'),
    path('products/', views.ProductListView.as_view(), name='product-list'),

]

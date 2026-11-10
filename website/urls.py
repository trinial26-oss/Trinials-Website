from django.urls import path
from . import views

app_name = 'website'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about_page, name='about_page'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-and-conditions/', views.terms_conditions, name='terms_conditions'),
    path('design-preview/', views.design_preview, name='design_preview'),
    path('contact/', views.contact_submit, name='contact'),
]

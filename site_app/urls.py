
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('apropos/', views.apropos, name='apropos'),
    path('programmes/', views.programmes, name='programmes'),
    path('actualites/', views.actualites, name='actualites'),
    path('admission/', views.admission, name='admission'),
    path('admission/formulaire/', views.admission_formulaire, name='admission_formulaire'),
    path('admission/formulaire/success/', views.admission_success, name='admission_success'),
    path('admission/formulaire/error/', views.admission_error, name='admission_error'),
    path('contact/', views.contact, name='contact'),
    path('nous-joindre/', views.nous_joindre, name='nous-joindre'),

]
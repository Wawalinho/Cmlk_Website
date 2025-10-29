
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('apropos/', views.apropos, name='apropos'),
    path('programmes/', views.programmes, name='programmes'),
    path('actualites/', views.actualites, name='actualites'),
    path('admission/', views.admission, name='admission'),
    path('admission/formulaire/', views.admission_formulaire, name='admission_formulaire'),
    path('admission/formulaire/confirmation/', views.admission_confirmation, name='admission_confirmation'),
    path('admission/formulaire/erreur/', views.admission_erreur, name='admission_erreur'),
    path('contact/', views.contact, name='contact'),
    path('nous-joindre/', views.nous_joindre, name='nous-joindre'),

]
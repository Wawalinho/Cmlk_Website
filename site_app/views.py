from django.shortcuts import render,redirect
from .models import Actualite
from .forms import AdmissionForm
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from django.core.mail import send_mail

def home(request):
    return render(request, 'home.html')

def apropos(request):
    return render(request, 'apropos.html')

def programmes(request):
    return render(request, 'programmes.html')

def actualites(request):
    actualites = Actualite.objects.all()
    return render(request, 'actualites.html', {'actualites': actualites})

def admission(request):
    return render(request, 'admission.html')

from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.contrib import messages
from .forms import AdmissionForm

def admission_formulaire(request):
    if request.method == 'POST':
        form = AdmissionForm(request.POST, request.FILES)
        if form.is_valid():
            admission = form.save()

            # --- Récupération des données principales ---
            nom = admission.nom
            email_user = admission.email
            niveau = admission.niveau_formation
            niveau_etude = admission.niveau_etude

            # --- Préparation du message pour le secrétariat ---
            subject_admin = f"Nouvelle demande d’admission - {nom}"
            message_admin = (
                f"Nom de l’élève : {nom}\n"
                f"Email : {email_user}\n"
                f"Niveau de formation : {niveau}\n"
                f"Niveau d’étude : {niveau_etude}\n\n"
                f"Une nouvelle demande d’admission vient d’être soumise via le site web."
            )

            try:
                # --- Envoi du mail au secrétariat ---
                send_mail(
                    subject_admin,
                    message_admin,
                    settings.DEFAULT_FROM_EMAIL,  # doit être défini dans settings.py
                    ['secretariat-cmlk@gmail.com'],
                    fail_silently=False,
                )

                # --- Message de confirmation à l’utilisateur ---
                subject_user = "Confirmation de réception de votre demande d’admission"
                message_user = (
                    f"Bonjour {nom},\n\n"
                    "Nous avons bien reçu votre demande d’admission au Collège Martin Luther King.\n"
                    "Notre secrétariat va examiner votre dossier et vous recevrez une réponse officielle sous peu.\n\n"
                    "Merci de votre confiance.\n\n"
                    "— Le secrétariat du Collège Martin Luther King"
                )

                send_mail(
                    subject_user,
                    message_user,
                    settings.DEFAULT_FROM_EMAIL,
                    [email_user],
                    fail_silently=False,
                )

                messages.success(request, "Votre demande a été soumise avec succès ! Vous recevrez un email de confirmation.")
                return redirect('admission_formulaire')

            except Exception as e:
                messages.error(request, f"Erreur lors de l’envoi de l’email : {e}")
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        form = AdmissionForm()

    return render(request, 'admission_formulaire.html', {'form': form})

def admission_success(request):
    return render(request, 'admission_success.html')

def admission_error(request):
    return render(request, 'admission_error.html')


            
def contact(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Message à envoyer à ton secrétariat
        sujet_admin = f"Nouveau message de contact de {nom}"
        contenu_admin = f"Nom : {nom}\nEmail : {email}\n\nMessage :\n{message}"

        try:
            # Envoi du message au secrétariat
            send_mail(
                sujet_admin,
                contenu_admin,
                settings.DEFAULT_FROM_EMAIL,
                ['secretariatcmlk@gmail.com'],
                fail_silently=False,
            )

            # Message automatique de confirmation pour l’utilisateur
            sujet_client = "Confirmation de réception - Collège Martin Luther King"
            contenu_client = (
                f"Bonjour {nom},\n\n"
                "Nous avons bien reçu votre message et vous remercions de nous avoir contactés.\n"
                "Notre équipe vous répondra dans les plus brefs délais.\n\n"
                "Cordialement,\n"
                "Le secrétariat du Collège Martin Luther King."
            )
            send_mail(
                sujet_client,
                contenu_client,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            messages.success(request, "Votre message a été envoyé avec succès !")
            return redirect('contact')

        except Exception as e:
            messages.error(request, f"Une erreur s'est produite : {e}")
            return redirect('contact')

    return render(request, 'contact.html')


def nous_joindre(request):
    categories = [
        "Programmes d'études",
        "Admission et inscription",
        "Emplois",
        "Services aux étudiants",
        "Informations générales"
    ]
    return render(request, 'nous_joindre.html', {'categories': categories})



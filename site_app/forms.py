from django import forms
from .models import Admission, NIVEAUX_ETUDE, NIVEAUX_FORMATION, Actualite



class ActualiteForm(forms.ModelForm):
    class Meta:
        model = Actualite
        fields = ['titre', 'description', 'image']
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre de l’actualité'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Description'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class AdmissionForm(forms.ModelForm):
    niveau_formation = forms.ChoiceField(
        choices=NIVEAUX_FORMATION,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    niveau_etude = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Admission
        fields = [
            'nom', 'date_naissance', 'email',
            'niveau_formation', 'niveau_etude',
            'acte_naissance', 'photo_identite', 'carte_vaccination',
            'carnet_pdf', 'bulletin_pdf', 'lettre_motivation',
            'paiement_pdf', 'commentaire'
        ]
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'date_naissance': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'commentaire': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Tous les champs de base requis
        self.fields['nom'].required = True
        self.fields['date_naissance'].required = True
        self.fields['email'].required = True
        self.fields['niveau_formation'].required = True
        self.fields['niveau_etude'].required = True

        # Documents non obligatoires par défaut
        for doc_field in [
            'acte_naissance', 'photo_identite', 'carte_vaccination',
            'carnet_pdf', 'bulletin_pdf', 'lettre_motivation', 'paiement_pdf'
        ]:
            self.fields[doc_field].required = False

        # Remplir dynamiquement les niveaux d'étude si possible
        formation = None
        if 'niveau_formation' in self.data:
            formation = self.data.get('niveau_formation')
        elif self.instance.pk:
            formation = self.instance.niveau_formation

        if formation and formation in NIVEAUX_ETUDE:
            self.fields['niveau_etude'].choices = NIVEAUX_ETUDE[formation]
        else:
            # Valeur par défaut vide pour éviter erreur d'affichage
            self.fields['niveau_etude'].choices = [('', '--- Sélectionnez un niveau ---')]

    def clean(self):
        cleaned_data = super().clean()
        formation = cleaned_data.get('niveau_formation')

        if not formation:
            self.add_error('niveau_formation', "Veuillez choisir un niveau de formation.")
            return cleaned_data

        # --- Règles de validation selon le niveau ---
        if formation == 'prescolaire':
            required_docs = ['acte_naissance', 'photo_identite', 'carte_vaccination']
        elif formation in ['fondamental_I', 'fondamental_II']:
            required_docs = ['acte_naissance', 'photo_identite', 'carnet_pdf']
        elif formation in ['fondamental_III', 'secondaire']:
            required_docs = ['acte_naissance', 'photo_identite', 'bulletin_pdf', 'lettre_motivation']
        else:
            required_docs = []

        # Vérifie que les documents obligatoires sont fournis
        for doc in required_docs:
            if not cleaned_data.get(doc):
                self.add_error(doc, f"Le document « {doc.replace('_', ' ').title()} » est obligatoire pour le niveau {formation.replace('_', ' ').title()}.")

        return cleaned_data

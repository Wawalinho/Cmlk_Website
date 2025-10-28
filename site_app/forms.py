from django import forms
from .models import Admission, NIVEAUX_ETUDE, NIVEAUX_FORMATION

class AdmissionForm(forms.ModelForm):
    niveau_formation = forms.ChoiceField(
        choices=NIVEAUX_FORMATION,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    niveau_etude = forms.ChoiceField(
        choices=[],  # sera rempli dynamiquement
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
        # Tous les champs requis par défaut
        for field in self.fields.values():
            field.required = True

        # Documents optionnels selon niveau
        for doc_field in ['acte_naissance', 'photo_identite', 'carte_vaccination', 'carnet_pdf', 'bulletin_pdf', 'lettre_motivation']:
            self.fields[doc_field].required = False

        # Si niveau_formation choisi, remplir les options de niveau_etude
        if 'niveau_formation' in self.data:
            formation = self.data.get('niveau_formation')
            self.fields['niveau_etude'].choices = NIVEAUX_ETUDE.get(formation, [])
        elif self.instance.pk:
            formation = self.instance.niveau_formation
            self.fields['niveau_etude'].choices = NIVEAUX_ETUDE.get(formation, [])

    # Validation dynamique des documents selon le niveau de formation/étude
    def clean(self):
        cleaned_data = super().clean()
        formation = cleaned_data.get('niveau_formation')

        if formation == 'prescolaire':
            required_docs = ['acte_naissance', 'photo_identite', 'carte_vaccination']
        elif formation in ['fondamental_I', 'fondamental_II']:
            required_docs = ['acte_naissance', 'photo_identite', 'carnet_pdf']
        elif formation in ['fondamental_III', 'secondaire']:
            required_docs = ['acte_naissance', 'photo_identite', 'bulletin_pdf', 'lettre_motivation']
        else:
            required_docs = []

        for doc in required_docs:
            if not cleaned_data.get(doc):
                self.add_error(doc, f"Ce document est obligatoire pour le niveau {formation.replace('_', ' ').title()}.")

        return cleaned_data


from django.db import models

class Actualite(models.Model):

    titre = models.CharField("Titre de l'actualité", max_length=200)
    description = models.TextField("Contenu ou description")
    image = models.ImageField("Image illustrant l'actualité", upload_to='actualites/')
    date_publication = models.DateField("Date de publication", auto_now_add=True)

    class Meta:
        ordering = ['-date_publication']
        verbose_name = ("Actualité")
        verbose_name_plural = ("Actualités")

    def __str__(self):
        return self.titre
    
# Niveaux de formation
NIVEAUX_FORMATION = [
    ('prescolaire', 'Préscolaire'),
    ('fondamental_I', 'Fondamental I'),
    ('fondamental_II', 'Fondamental II'),
    ('fondamental_III', 'Fondamental III'),
    ('secondaire', 'Secondaire'),
]

# Niveaux d'étude par formation
NIVEAUX_ETUDE = {
    'prescolaire': [('jardin_I', 'Jardin I'), ('jardin_II', 'Jardin II'), ('jardin_III', 'Jardin III')],
    'fondamental_I': [('1_AF', '1 AF'), ('2_AF', '2 AF'), ('3_AF', '3 AF'), ('4_AF', '4 AF')],
    'fondamental_II': [('5_AF', '5 AF'), ('6_AF', '6 AF')],
    'fondamental_III': [('7_AF', '7 AF'), ('8_AF', '8 AF'), ('9_AF', '9 AF')],
    'secondaire': [('sec_I', 'Secondaire I'), ('sec_II', 'Secondaire II'), ('sec_III', 'Secondaire III'), ('sec_IV', 'Secondaire IV')],
}

class Admission(models.Model):
    nom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    niveau_formation = models.CharField(max_length=50, choices=NIVEAUX_FORMATION)
    niveau_etude = models.CharField(max_length=50)
    email = models.EmailField()

    # Documents
    acte_naissance = models.FileField(upload_to='documents/', blank=True, null=True)
    photo_identite = models.FileField(upload_to='documents/', blank=True, null=True)
    carte_vaccination = models.FileField(upload_to='documents/', blank=True, null=True)
    carnet_pdf = models.FileField(upload_to='documents/', blank=True, null=True)
    bulletin_pdf = models.FileField(upload_to='documents/', blank=True, null=True)
    lettre_motivation = models.FileField(upload_to='documents/', blank=True, null=True)
    paiement_pdf = models.FileField(upload_to='documents/', blank=True, null=True)

    commentaire = models.TextField(blank=True, null=True)
    date_soumission = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Demande d'admission - {self.nom}"

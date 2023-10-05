from django.db import models
from django.db import models
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver


class Facture(models.Model):
    
    nom_patient = models.CharField(max_length=100)
    prenom_patient = models.CharField(max_length=100)
    caisse = models.CharField(max_length=100)
    date = models.DateField()
    reduction = models.DecimalField(max_digits=10, decimal_places=2)
    montant_paye = models.DecimalField(max_digits=10, decimal_places=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    montant_remis = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    examen = models.CharField(max_length=100)
    encaisse = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    mode_paiement = models.CharField(max_length=100, default="Cash") 

    def __str__(self):
        return f"Facture de {self.nom_patient} {self.prenom_patient}"


from django.db import models
from AppCaisse.models import Facture

class Dette(models.Model):
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    examen = models.CharField(max_length=100)
    date = models.DateField()
    caisse = models.CharField(max_length=100)    

    def __str__(self):
        return f"Dette de {self.nom} {self.prenom}"

class Comptabilite(models.Model):
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    examen = models.CharField(max_length=100)
    date = models.DateField()
    caisse = models.CharField(max_length=100)

from django.db import models

class RetraitCaisse(models.Model):
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    caisse = models.CharField(max_length=100, default='Secretariat')
    date = models.DateTimeField(auto_now_add=True)
    motif = models.TextField()

@receiver(post_save, sender=RetraitCaisse)
def mise_a_jour_montant_par_date(sender, instance, **kwargs):
    date_retrait = instance.date.date()
    montant = instance.montant
    montant_obj, created = MontantParDate.objects.get_or_create(date=date_retrait)
    
    # Si l'objet MontantParDate existe déjà pour cette date, mettez à jour le montant
    if not created:
        montant_obj.montant += montant
    else:
        montant_obj.montant = montant  # Spécifiez la valeur du montant ici
    
    montant_obj.save()


    def __str__(self):
        return f"Retrait de {self.montant} le {self.date}"
    
from django.db import models

class ResultatCalcul(models.Model):
    jour = models.DateField()
    caisse = models.CharField(max_length=100)
    somme_disponible = models.DecimalField(max_digits=10, decimal_places=2)
  
from django.db import models
from decimal import Decimal
from AppCaisse.models import RetraitCaisse


from django.db import models, transaction
from django.db.models import Sum
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models import Sum

class MontantParDate(models.Model):
    date = models.DateField(unique=True)
    montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return str(self.date)

@receiver(post_save, sender=RetraitCaisse)
def update_montant_par_date(sender, instance, **kwargs):
    date_retrait = instance.date.date()

    # Calculez la somme des montants des retraits pour la date du retrait
    montant_total = RetraitCaisse.objects.filter(date__date=date_retrait).aggregate(Sum('montant'))['montant__sum'] or 0.00

    # Vérifiez si une instance MontantParDate existe pour cette date
    montant_obj, created = MontantParDate.objects.get_or_create(date=date_retrait)

    # Mettez à jour le montant dans MontantParDate
    montant_obj.montant = montant_total
    montant_obj.save()


from django.db import models

class EntreeParDate(models.Model):
    date = models.DateField(unique=True)
    montant_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return str(self.date)


from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Comptabilite, EntreeParDate

@receiver(post_save, sender=Comptabilite)
def update_entree_par_date(sender, instance, **kwargs):
    date_comptabilite = instance.date

    # Calculez la somme des montants des entrées pour la date de la comptabilité
    montant_total = Comptabilite.objects.filter(date=date_comptabilite).aggregate(Sum('montant'))['montant__sum'] or 0.00

    # Vérifiez si une instance EntreeParDate existe pour cette date
    entree_obj, created = EntreeParDate.objects.get_or_create(date=date_comptabilite)

    # Mettez à jour le montant dans EntreeParDate
    entree_obj.montant_total = montant_total
    entree_obj.save()


from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class CashParJour(models.Model):
    date = models.DateField(unique=True)
    difference_cash = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return str(self.date)


@receiver(post_save, sender=EntreeParDate)
@receiver(post_save, sender=MontantParDate)
def update_cash_par_jour(sender, instance, **kwargs):
    # Obtenez la date de l'instance mise à jour
    date = instance.date

    # Obtenez le modèle CashParJour correspondant ou créez-le s'il n'existe pas
    cash_par_jour, created = CashParJour.objects.get_or_create(date=date)

    # Obtenez les montants des autres modèles s'ils existent
    montant_entree = EntreeParDate.objects.filter(date=date).first()
    montant_sortie = MontantParDate.objects.filter(date=date).first()

    # Vérifiez si les montants existent avant de les soustraire
    if montant_entree and montant_sortie:
        difference_cash = montant_entree.montant_total - montant_sortie.montant
    elif montant_entree:
        difference_cash = montant_entree.montant_total
    elif montant_sortie:
        difference_cash = -montant_sortie.montant
    else:
        difference_cash = 0.0

    # Mettez à jour la différence en espèces dans le modèle CashParJour
    cash_par_jour.difference_cash = difference_cash
    cash_par_jour.save()

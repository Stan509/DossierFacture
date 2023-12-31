# Generated by Django 4.1.5 on 2023-10-05 04:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CashParJour",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField(unique=True)),
                (
                    "difference_cash",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
                ),
            ],
        ),
        migrations.CreateModel(
            name="EntreeParDate",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField(unique=True)),
                (
                    "montant_total",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Facture",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nom_patient", models.CharField(max_length=100)),
                ("prenom_patient", models.CharField(max_length=100)),
                ("caisse", models.CharField(max_length=100)),
                ("date", models.DateField()),
                ("reduction", models.DecimalField(decimal_places=2, max_digits=10)),
                ("montant_paye", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "balance",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                (
                    "montant_remis",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                (
                    "prix",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                (
                    "total",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                ("examen", models.CharField(max_length=100)),
                (
                    "encaisse",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
                ),
                ("mode_paiement", models.CharField(default="Cash", max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="MontantParDate",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField(unique=True)),
                (
                    "montant",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ResultatCalcul",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("jour", models.DateField()),
                ("caisse", models.CharField(max_length=100)),
                (
                    "somme_disponible",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
            ],
        ),
        migrations.CreateModel(
            name="RetraitCaisse",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("montant", models.DecimalField(decimal_places=2, max_digits=10)),
                ("caisse", models.CharField(default="Secretariat", max_length=100)),
                ("date", models.DateTimeField(auto_now_add=True)),
                ("motif", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="Dette",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nom", models.CharField(max_length=100)),
                ("prenom", models.CharField(max_length=100)),
                ("montant", models.DecimalField(decimal_places=2, max_digits=10)),
                ("examen", models.CharField(max_length=100)),
                ("date", models.DateField()),
                ("caisse", models.CharField(max_length=100)),
                (
                    "facture",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="AppCaisse.facture",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Comptabilite",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nom", models.CharField(max_length=100)),
                ("prenom", models.CharField(max_length=100)),
                ("montant", models.DecimalField(decimal_places=2, max_digits=10)),
                ("examen", models.CharField(max_length=100)),
                ("date", models.DateField()),
                ("caisse", models.CharField(max_length=100)),
                (
                    "facture",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="AppCaisse.facture",
                    ),
                ),
            ],
        ),
    ]

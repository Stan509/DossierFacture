"""
URL configuration for ProjetCaisse project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from AppCaisse import views
from django.urls import path
from django.contrib.auth.decorators import login_required
from AppCaisse.views import FacturePDFView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', login_required(views.acceuil), name='acceuil'),
    path('enregistrer_facture/', views.enregistrer_facture, name='enregistrer_facture'),
    path('facture_pdf/<int:facture_id>/', FacturePDFView.as_view(), name='facture_pdf'),
    path('dette/', login_required(views.liste_dette), name='liste_dette'),
    path('liste_et_ajout_dette/', views.liste_et_ajout_dette, name='liste_et_ajout_dette'),
    path('supprimer_dette/<int:dette_id>/', views.supprimer_dette, name='supprimer_dette'),
    path('modifier_dette/<int:dette_id>/', views.modifier_dette, name='modifier_dette'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('retraits/', login_required(views.page_retraits), name='page_retraits'),
    path('comptabilite/', login_required(views.comptabilite), name='comptabilite'),
    path('calcul_somme_disponible/', views.calcul_somme_disponible, name='calcul_somme_disponible'),
    path('cashparjour/', views.cashparjour_view, name='cashparjour_view'),

]

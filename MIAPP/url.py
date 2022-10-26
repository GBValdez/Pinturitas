from django.urls import path
from . import views
urlpatterns = [
    path("",views.Login),
    path("Autenticacion/",views.Revisar,name="Autenticacion")
]
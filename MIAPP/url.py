from django.urls import path
from . import views
#Las url del login
urlpatterns = [
    path("",views.Login),
    path("Autenticacion/",views.Revisar,name="Autenticacion")
]
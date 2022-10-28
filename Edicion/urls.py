from unicodedata import name
from django.urls import path
from . import views 
app_name="Edicion"
urlpatterns = [
    path('Bodegas/<int:ID>', views.Bodega_edicio,name="Bodegas"),
    path('Usuarios/<int:ID>', views.Usuario_edicion,name="Usuario"),
    path('Contactos/<str:Tipo>/<int:ID>', views.Contactos_edicion,name="Contactos"),
    path('Movimiento/<str:Tipo>/<int:Clase>/<str:Salida>/<int:ID>', views.Movimiento_Edicion,name="Movimiento"),
    path('Productos/<int:ID>', views.Producto_edicion,name="Productos"),
    path('Ingresar/<str:Tipo>',views.Ingresar,name="Ingresar"),
    path('Ingresar_unico/<str:Nom_Archivo>/<str:Valor>/<str:Vista>/<int:ID>',views.Ingresar_unicos,name="Ingresar_Unico"),  # type: ignore
    
]
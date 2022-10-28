from django.urls import path
from . import views 
urlpatterns = [
    path('Bodegas', views.Bodegas_Consultas,name="Bodegas_Consulta"),
    path('Contactos/<int:Tipo>',views.Contactos_Consultas,name="Contactos_Consulta"),
    path('Facturas/',views.Facturas_Consulta,name="Facturas_Consulta"),
    path('Movimiento/<int:Tipo>',views.Movimiento_Consulta,name="Movimiento_Consulta"),
    path('Producto_Consulta',views.Producto_Consulta,name="Producto_Consulta"),
    path('Reporte_Inventario',views.Reporte_Inventario,name="Reporte_Inventario"),
    path('Usuarios',views.Usuario_Consulta,name="Usuarios_Consulta")
]
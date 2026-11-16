from django.urls import path
from . import views

urlpatterns = [
    # Estado del Backend API
    path('', views.estado_api, name='estado_api'),

    # Catálogo
    path('api/catalogo/', views.listar_catalogo, name='listar_catalogo'),
    path('api/catalogo/<int:id>/', views.detalle_herramienta, name='detalle_herramienta'),

    # Recomendador IA y Reglas
    path('api/recomendar/', views.recomendar_herramienta, name='recomendar_herramienta'),

    # Rentas con Folio
    path('api/rentas/', views.registrar_renta, name='registrar_renta'),
    path('api/rentas/<str:folio>/', views.consultar_renta_por_folio, name='consultar_renta_por_folio'),

    # Asistente inteligente
    path('api/asistente/', views.asistente_chat, name='asistente_chat'),
]

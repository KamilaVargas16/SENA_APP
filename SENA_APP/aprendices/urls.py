from django.urls import path
from . import views 

app_name = 'aprendices'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('aprendices/', views.aprendices, name='lista_aprendices'),
    path('aprendices/aprendiz/<int:id_aprendiz>/', views.detalle_aprendiz, name='detalle_aprendiz'),
    path('aprendices/crear/', views.AprendizCreateView.as_view(), name='crear_aprendiz'),
    path('aprendices/<int:aprendiz_id>/editar/', views.AprendizUpdateView.as_view(), name='editar_aprendiz'),
    path('aprendices/<int:aprendiz_id>/eliminar/', views.AprendizDeleteView.as_view(), name='eliminar_aprendiz'),
]
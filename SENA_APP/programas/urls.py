from django.urls import path
from . import views 

app_name = 'programas'

urlpatterns = [
    path('', views.lista_programa, name='lista_programa'),
    path('<int:id_programas>/', views.detalle_programa, name='detalle_programa'),
]

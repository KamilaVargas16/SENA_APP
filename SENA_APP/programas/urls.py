from django.urls import path
from . import views 

app_name = 'programas'

urlpatterns = [
    path('', views.lista_programa, name='lista_programa'),
    path('<int:id_programas>/', views.detalle_programa, name='detalle_programa'),
    path('crear/', views.ProgramaCreateView.as_view(), name='crear_programa'),
    path('<int:programa_id>/editar/', views.ProgramaUpdateView.as_view(), name='editar_programa'),
    path('<int:programa_id>/eliminar/', views.ProgramaDeleteView.as_view(), name='eliminar_programa'),
]

from django.urls import path
from . import views 

app_name = 'cursos'

urlpatterns = [
    path('', views.lista_cursos, name='lista_cursos'),
    path('<int:curso_id>/', views.detalle_curso, name='detalle_curso'),
]
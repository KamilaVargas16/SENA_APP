from django.urls import path
from . import views 

app_name = 'instructores'

urlpatterns = [
    path('', views.lista_instructores, name='lista_instructores'),
    path('<int:id_instructor>/', views.detalle_instructor, name='detalle_instructor'),
    path('crear/', views.InstructorCreateView.as_view(), name='crear_instructor'),
    path('<int:instructor_id>/editar/', views.InstructorUpdateView.as_view(), name='editar_instructor'),
    path('<int:instructor_id>/eliminar/', views.InstructorDeleteView.as_view(), name='eliminar_instructor'),
]
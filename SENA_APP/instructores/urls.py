from django.urls import path
from . import views 

app_name = 'instructores'

urlpatterns = [
    path('', views.lista_instructores, name='lista_instructores'),
    path('<int:id_instructor>/', views.detalle_instructor, name='detalle_instructor'),
]
from django.template import loader
from django.http import HttpResponse
from .models import Instructor

# Create your views here.

def lista_instructores(request):
    # Usar queryset de instancias (no .values()) para que las plantillas
    # puedan acceder a atributos y métodos del modelo si es necesario.
    lista_instructores = Instructor.objects.all()
    template = loader.get_template('lista_instructores.html')
    context = {
        'lista_instructores': lista_instructores,
    }
    return HttpResponse(template.render(context, request))

def detalle_instructor(request, id_instructor):
    # Alinear el nombre del parámetro con la URL y pasar la clave 'instructor'
    instructor = Instructor.objects.get(id=id_instructor)
    template = loader.get_template('detalle_instructor.html')
    context = {
        'instructor': instructor,
    }
    return HttpResponse(template.render(context, request))

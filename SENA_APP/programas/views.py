from django.http import HttpResponse
from django.template import loader
from .models import Programa

# Create your views here.

def main(request):
    template = loader.get_template("main.html")
    return HttpResponse(template.render())

def lista_programa(request):
    lista_programas = Programa.objects.all()
    template = loader.get_template("lista_programa.html")
    context = {
        "lista_programas": lista_programas,
        'total_programa': lista_programas.count(),
    }
    return HttpResponse(template.render(context, request))


def detalle_programa(request, id_programas):
    detalle_programa = Programa.objects.get(id=id_programas)
    template = loader.get_template("detalle_programa.html")
    context = {
        "programa": detalle_programa,
    }
    return HttpResponse(template.render(context, request))
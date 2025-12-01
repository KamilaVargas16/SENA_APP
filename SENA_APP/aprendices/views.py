from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from .models import Aprendiz

# Create your views here.

def aprendices(request):
    lista_aprendices = Aprendiz.objects.all()
    template = loader.get_template('lista_aprendices.html')
    
    context = {
        'lista_aprendices': lista_aprendices,
    }
    return HttpResponse(template.render(context, request))

def detalle_aprendiz(request, id_aprendiz):
  aprendiz = Aprendiz.objects.get(id=id_aprendiz)
  template = loader.get_template('detalle_aprendiz.html')
  context = {
    'aprendiz': aprendiz,
  }
  return HttpResponse(template.render(context, request))

def inicio(request):
  template = loader.get_template('main.html')
  return HttpResponse(template.render())
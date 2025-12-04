from django.shortcuts import render
from django.template import loader
from .models import Curso
from django.http import HttpResponse

# Create your views here.
def lista_cursos(request):
    cursos = Curso.objects.all()
    template = loader.get_template('lista_cursos.html')

    context = {
        'lista_cursos': cursos,
        'total_cursos': cursos.count(),
    }
    
    return HttpResponse(template.render(context, request))

def detalle_curso(request, curso_id):
    curso = Curso.objects.get(id=curso_id)
    aprendices_curso = curso.aprendizcurso_set.all()
    instructores_curso = curso.instructorcurso_set.all()
    template = loader.get_template('detalle_curso.html')
    
    context = {
        'curso': curso,
        'aprendices_curso': aprendices_curso,
        'instructores_curso': instructores_curso,
    }
    
    return HttpResponse(template.render(context, request))
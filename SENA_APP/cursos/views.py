from pyexpat.errors import messages
from django.shortcuts import render
from django.template import loader
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages

from .forms import CursoForm
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


# CREATE - CURSO
class CursoCreateView(generic.CreateView):
    """Vista para crear un nuevo curso"""
    model = Curso
    form_class = CursoForm
    template_name = 'agregar_curso.html'
    success_url = reverse_lazy('cursos:lista_cursos')
    
    def form_valid(self, form):
        """Mostrar mensaje de éxito al crear el curso"""
        messages.success(
            self.request,
            f'El curso "{form.instance.nombre}" (Código: {form.instance.codigo}) ha sido registrado exitosamente.'
        )
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """Mostrar mensaje de error si el formulario es inválido"""
        messages.error(
            self.request,
            'Por favor, corrija los errores en el formulario.'
        )
        return super().form_invalid(form)


# UPDATE - CURSO
class CursoUpdateView(generic.UpdateView):
    """Vista para actualizar un curso existente"""
    model = Curso
    form_class = CursoForm
    template_name = 'editar_curso.html'
    success_url = reverse_lazy('cursos:lista_cursos')
    pk_url_kwarg = 'curso_id'
    
    def form_valid(self, form):
        """Mostrar mensaje de éxito al actualizar"""
        messages.success(
            self.request,
            f'El curso "{form.instance.nombre}" ha sido actualizado exitosamente.'
        )
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """Mostrar mensaje de error si el formulario es inválido"""
        messages.error(
            self.request,
            'Por favor, corrija los errores en el formulario.'
        )
        return super().form_invalid(form)


# DELETE - CURSO
class CursoDeleteView(generic.DeleteView):
    """Vista para eliminar un curso"""
    model = Curso
    template_name = 'eliminar_curso.html'
    success_url = reverse_lazy('cursos:lista_cursos')
    pk_url_kwarg = 'curso_id'
    
    def delete(self, request, *args, **kwargs):
        """Mostrar mensaje de éxito al eliminar"""
        curso = self.get_object()
        messages.success(
            request,
            f'El curso "{curso.nombre}" (Código: {curso.codigo}) ha sido eliminado exitosamente.'
        )
        return super().delete(request, *args, **kwargs)
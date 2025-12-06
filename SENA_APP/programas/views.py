from django.http import HttpResponse
from django.template import loader
from .models import Programa
from django.views import generic
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Programa
from .forms import ProgramaForm

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

# CREATE - PROGRAMA
class ProgramaCreateView(generic.CreateView):
    """Vista para crear un nuevo programa de formación"""
    model = Programa
    form_class = ProgramaForm
    template_name = 'agregar_programa.html'
    success_url = reverse_lazy('programas:lista_programa')
    
    def form_valid(self, form):
        """Mostrar mensaje de éxito al crear el programa"""
        messages.success(
            self.request,
            f'El programa "{form.instance.nombre}" ha sido registrado exitosamente.'
        )
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """Mostrar mensaje de error si el formulario es inválido"""
        messages.error(
            self.request,
            'Por favor, corrija los errores en el formulario.'
        )
        return super().form_invalid(form)


# UPDATE - PROGRAMA
class ProgramaUpdateView(generic.UpdateView):
    """Vista para actualizar un programa existente"""
    model = Programa
    form_class = ProgramaForm
    template_name = 'editar_programa.html'
    success_url = reverse_lazy('programas:lista_programa')
    pk_url_kwarg = 'programa_id'
    
    def form_valid(self, form):
        """Mostrar mensaje de éxito al actualizar"""
        messages.success(
            self.request,
            f'El programa "{form.instance.nombre}" ha sido actualizado exitosamente.'
        )
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """Mostrar mensaje de error si el formulario es inválido"""
        messages.error(
            self.request,
            'Por favor, corrija los errores en el formulario.'
        )
        return super().form_invalid(form)


# DELETE - PROGRAMA
class ProgramaDeleteView(generic.DeleteView):
    """Vista para eliminar un programa"""
    model = Programa
    template_name = 'eliminar_programa.html'
    success_url = reverse_lazy('programas:lista_programa')
    pk_url_kwarg = 'programa_id'
    
    def delete(self, request, *args, **kwargs):
        """Mostrar mensaje de éxito al eliminar"""
        programa = self.get_object()
        messages.success(
            request,
            f'El programa "{programa.nombre}" (Código: {programa.codigo}) ha sido eliminado exitosamente.'
        )
        return super().delete(request, *args, **kwargs)
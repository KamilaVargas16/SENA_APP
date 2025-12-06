from django.template import loader
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib import messages

from .forms import InstructorForm
from .models import Instructor

# Create your views here.

def lista_instructores(request):
    
    lista_instructores = Instructor.objects.all()
    template = loader.get_template('lista_instructores.html')
    context = {
        'lista_instructores': lista_instructores,
    }
    return HttpResponse(template.render(context, request))

def detalle_instructor(request, id_instructor):
    
    instructor = Instructor.objects.get(id=id_instructor)
    template = loader.get_template('detalle_instructor.html')
    context = {
        'instructor': instructor,
    }
    return HttpResponse(template.render(context, request))

# CREATE - INSTRUCTOR
class InstructorCreateView(CreateView):
    """Vista para crear un nuevo instructor"""
    model = Instructor
    form_class = InstructorForm
    template_name = 'agregar_instructor.html'
    success_url = reverse_lazy('instructores:lista_instructores')
    
    def form_valid(self, form):
        """Mostrar mensaje de éxito al crear el instructor"""
        messages.success(
            self.request,
            f'El instructor {form.instance.nombre} {form.instance.apellido} ha sido registrado exitosamente.'
        )
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """Mostrar mensaje de error si el formulario es inválido"""
        messages.error(
            self.request,
            'Por favor, corrija los errores en el formulario.'
        )
        return super().form_invalid(form)


# UPDATE - INSTRUCTOR
class InstructorUpdateView(UpdateView):
    """Vista para actualizar un instructor existente"""
    model = Instructor
    form_class = InstructorForm
    template_name = 'editar_instructor.html'
    success_url = reverse_lazy('instructores:lista_instructores')
    pk_url_kwarg = 'instructor_id'
    
    def form_valid(self, form):
        """Mostrar mensaje de éxito al actualizar"""
        messages.success(
            self.request,
            f'El instructor {form.instance.nombre} {form.instance.apellido} ha sido actualizado exitosamente.'
        )
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """Mostrar mensaje de error si el formulario es inválido"""
        messages.error(
            self.request,
            'Por favor, corrija los errores en el formulario.'
        )
        return super().form_invalid(form)


# DELETE - INSTRUCTOR
class InstructorDeleteView(DeleteView):
    """Vista para eliminar un instructor"""
    model = Instructor
    template_name = 'eliminar_instructor.html'
    success_url = reverse_lazy('instructores:lista_instructores')
    pk_url_kwarg = 'instructor_id'
    
    def delete(self, request, *args, **kwargs):
        """Mostrar mensaje de éxito al eliminar"""
        instructor = self.get_object()
        messages.success(
            request,
            f'El instructor {instructor.nombre} {instructor.apellido} ha sido eliminado exitosamente.'
        )
        return super().delete(request, *args, **kwargs)


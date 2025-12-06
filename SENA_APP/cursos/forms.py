from django import forms
from .models import Curso, InstructorCurso, AprendizCurso
from programas.models import Programa
from instructores.models import Instructor
from aprendices.models import Aprendiz


class CursoForm(forms.ModelForm):
    """Formulario basado en modelo para crear y editar cursos"""
    
    class Meta:
        model = Curso
        fields = [
            'codigo',
            'nombre',
            'programa',
            'instructor_coordinador',
            'fecha_inicio',
            'fecha_fin',
            'horario',
            'aula',
            'cupos_maximos',
            'estado',
            'observaciones'
        ]
        # Widgets personalizados para mejorar la interfaz en el HTML
        widgets = {
            'codigo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: CURSO-2024-001'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre del curso'
            }),
            'programa': forms.Select(attrs={
                'class': 'form-control'
            }),
            'instructor_coordinador': forms.Select(attrs={
                'class': 'form-control'
            }),
            'fecha_inicio': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'fecha_fin': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'horario': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Lunes a Viernes 8:00 AM - 12:00 PM'
            }),
            'aula': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Aula 101, Lab 203'
            }),
            'cupos_maximos': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número máximo de aprendices',
                'min': 1
            }),
            'estado': forms.Select(attrs={
                'class': 'form-control'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Observaciones adicionales sobre el curso',
                'rows': 3
            })
        }
        # Etiquetas personalizadas
        labels = {
            'codigo': 'Código del Curso',
            'nombre': 'Nombre del Curso',
            'programa': 'Programa de Formación',
            'instructor_coordinador': 'Instructor Coordinador',
            'fecha_inicio': 'Fecha de Inicio',
            'fecha_fin': 'Fecha de Finalización',
            'horario': 'Horario',
            'aula': 'Aula/Ambiente',
            'cupos_maximos': 'Cupos Máximos',
            'estado': 'Estado del Curso',
            'observaciones': 'Observaciones'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo programas activos
        self.fields['programa'].queryset = Programa.objects.filter(estado='ACT').order_by('nombre')
        # Filtrar solo instructores activos
        self.fields['instructor_coordinador'].queryset = Instructor.objects.filter(activo=True).order_by('apellido', 'nombre')

    # Validaciones personalizadas
    
    def clean_codigo(self):
        """Validar formato del código del curso"""
        codigo = self.cleaned_data.get('codigo')
        if not codigo:
            raise forms.ValidationError("El código es obligatorio.")
        
        # Convertir a mayúsculas
        codigo = codigo.upper().strip()
        
        # Validar que no contenga caracteres especiales peligrosos
        if any(char in codigo for char in ['<', '>', '"', "'"]):
            raise forms.ValidationError("El código contiene caracteres no permitidos.")
        
        return codigo
    
    def clean_cupos_maximos(self):
        """Validar que los cupos máximos sean razonables"""
        cupos = self.cleaned_data.get('cupos_maximos')
        
        if cupos and cupos < 5:
            raise forms.ValidationError("Los cupos mínimos deben ser al menos 5.")
        
        if cupos and cupos > 100:
            raise forms.ValidationError("Los cupos máximos no pueden exceder 100.")
        
        return cupos
    
    def clean(self):
        """Validaciones que involucran múltiples campos"""
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')
        programa = cleaned_data.get('programa')
        
        # Validar que la fecha de fin sea posterior a la fecha de inicio
        if fecha_inicio and fecha_fin:
            if fecha_fin <= fecha_inicio:
                raise forms.ValidationError(
                    "La fecha de finalización debe ser posterior a la fecha de inicio."
                )
            
            # Validar que la duración sea razonable (máximo 2 años)
            duracion_dias = (fecha_fin - fecha_inicio).days
            if duracion_dias > 730:  # 2 años
                self.add_error('fecha_fin', 
                    "La duración del curso parece demasiado larga. Verifique las fechas.")
        
        return cleaned_data


class InstructorCursoForm(forms.ModelForm):
    """Formulario para asignar instructores a cursos"""
    
    class Meta:
        model = InstructorCurso
        fields = ['instructor', 'curso', 'rol']
        widgets = {
            'instructor': forms.Select(attrs={
                'class': 'form-control'
            }),
            'curso': forms.Select(attrs={
                'class': 'form-control'
            }),
            'rol': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Instructor de Práctica, Instructor Técnico'
            })
        }
        labels = {
            'instructor': 'Instructor',
            'curso': 'Curso',
            'rol': 'Rol en el Curso'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo instructores activos
        self.fields['instructor'].queryset = Instructor.objects.filter(activo=True).order_by('apellido', 'nombre')


class AprendizCursoForm(forms.ModelForm):
    """Formulario para inscribir aprendices en cursos"""
    
    class Meta:
        model = AprendizCurso
        fields = ['aprendiz', 'curso', 'estado', 'nota_final', 'observaciones']
        widgets = {
            'aprendiz': forms.Select(attrs={
                'class': 'form-control'
            }),
            'curso': forms.Select(attrs={
                'class': 'form-control'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-control'
            }),
            'nota_final': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nota de 0.0 a 5.0',
                'step': '0.1',
                'min': '0.0',
                'max': '5.0'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Observaciones sobre el desempeño del aprendiz',
                'rows': 3
            })
        }
        labels = {
            'aprendiz': 'Aprendiz',
            'curso': 'Curso',
            'estado': 'Estado en el Curso',
            'nota_final': 'Nota Final',
            'observaciones': 'Observaciones'
        }
    
    def clean_nota_final(self):
        """Validar que la nota esté en el rango correcto"""
        nota = self.cleaned_data.get('nota_final')
        
        if nota is not None:
            if nota < 0.0 or nota > 5.0:
                raise forms.ValidationError("La nota debe estar entre 0.0 y 5.0")
        
        return nota
    
    def clean(self):
        """Validar que el curso no exceda los cupos máximos"""
        cleaned_data = super().clean()
        curso = cleaned_data.get('curso')
        aprendiz = cleaned_data.get('aprendiz')
        
        # Si es una nueva inscripción (no una actualización)
        if curso and aprendiz and not self.instance.pk:
            # Verificar cupos disponibles
            if curso.cupos_disponibles() <= 0:
                raise forms.ValidationError(
                    f"El curso {curso.codigo} no tiene cupos disponibles."
                )
        
        return cleaned_data
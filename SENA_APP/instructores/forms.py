from django import forms
from .models import Instructor


class InstructorForm(forms.ModelForm):
    """Formulario basado en modelo para crear y editar instructores"""
    
    class Meta:
        model = Instructor
        fields = [
            'tipo_documento',
            'documento_id',
            'nombre',
            'apellido',
            'telefono',
            'correo',
            'fecha_nacimiento',
            'ciudad',
            'direccion',
            'nivel_educativo',
            'especialidad',
            'anos_experiencia',
            'activo',
            'fecha_vinculacion'
        ]
      
        widgets = {
            'tipo_documento': forms.Select(attrs={
                'class': 'form-control'
            }),
            'documento_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el número de documento'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre'
            }),
            'apellido': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el apellido'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '3001234567'
            }),
            'correo': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com'
            }),
            'fecha_nacimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'ciudad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ciudad de residencia'
            }),
            'direccion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Dirección completa',
                'rows': 3
            }),
            'nivel_educativo': forms.Select(attrs={
                'class': 'form-control'
            }),
            'especialidad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Área de especialización'
            }),
            'anos_experiencia': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Años de experiencia',
                'min': 0
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'fecha_vinculacion': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            })
        }
        
        labels = {
            'tipo_documento': 'Tipo de Documento',
            'documento_id': 'Número de Documento',
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'telefono': 'Teléfono',
            'correo': 'Correo Electrónico',
            'fecha_nacimiento': 'Fecha de Nacimiento',
            'ciudad': 'Ciudad',
            'direccion': 'Dirección',
            'nivel_educativo': 'Nivel Educativo',
            'especialidad': 'Especialidad',
            'anos_experiencia': 'Años de Experiencia',
            'activo': 'Activo',
            'fecha_vinculacion': 'Fecha de Vinculación'
        }

    
    def clean_documento_id(self):
        """Validar que el documento contenga solo números o formato válido"""
        documento_id = self.cleaned_data.get('documento_id')
        tipo_documento = self.cleaned_data.get('tipo_documento')
        
        if tipo_documento in ['CC', 'CE', 'TI']:
            if not documento_id.isdigit():
                raise forms.ValidationError("El documento debe contener solo números.")
        
        return documento_id

    def clean_telefono(self):
        """Validar que el teléfono contenga solo números"""
        telefono = self.cleaned_data.get('telefono')
        if telefono and not telefono.isdigit():
            raise forms.ValidationError("El teléfono debe contener solo números.")
        if telefono and len(telefono) != 10:
            raise forms.ValidationError("El teléfono debe tener 10 dígitos.")
        return telefono
    
    def clean_anos_experiencia(self):
        """Validar que los años de experiencia sean razonables"""
        anos = self.cleaned_data.get('anos_experiencia')
        if anos and anos > 50:
            raise forms.ValidationError("Los años de experiencia parecen demasiado altos.")
        return anos
    
    def clean(self):
        """Validaciones que involucran múltiples campos"""
        cleaned_data = super().clean()
        fecha_nacimiento = cleaned_data.get('fecha_nacimiento')
        fecha_vinculacion = cleaned_data.get('fecha_vinculacion')
        
        if fecha_nacimiento and fecha_vinculacion:
            if fecha_vinculacion <= fecha_nacimiento:
                raise forms.ValidationError(
                    "La fecha de vinculación debe ser posterior a la fecha de nacimiento."
                )
        
        return cleaned_data
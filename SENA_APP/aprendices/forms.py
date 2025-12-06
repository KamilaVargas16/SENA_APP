from django import forms
from .models import Aprendiz


class AprendizForm(forms.ModelForm):
    """Formulario basado en modelo para crear y editar aprendices"""
    
    class Meta:
        model = Aprendiz
        fields = [
            'document',
            'firstname',
            'lastname',
            'phone',
            'email',
            'birthdate',
            'city',
            'program'
        ]
        # Widgets personalizados para mejorar la interfaz en el HTML
        widgets = {
            'document': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el documento'
            }),
            'firstname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre'
            }),
            'lastname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el apellido'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '3001234567'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com'
            }),
            'birthdate': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ciudad de residencia'
            }),
            'program': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Programa de formación'
            })
        }
        # Etiquetas personalizadas
        labels = {
            'document': 'Documento de Identidad',
            'firstname': 'Nombre',
            'lastname': 'Apellido',
            'phone': 'Teléfono',
            'email': 'Correo Electrónico',
            'birthdate': 'Fecha de Nacimiento',
            'city': 'Ciudad',
            'program': 'Programa'
        }

    # Validaciones personalizadas
    
    def clean_document(self):
        """Validar que el documento contenga solo números"""
        document = self.cleaned_data.get('document')
        if not document.isdigit():
            raise forms.ValidationError("El documento debe contener solo números.")
        return document

    def clean_phone(self):
        """Validar que el teléfono contenga solo números"""
        phone = self.cleaned_data.get('phone')
        if phone and not phone.isdigit():
            raise forms.ValidationError("El teléfono debe contener solo números.")
        if phone and len(phone) != 10:
            raise forms.ValidationError("El teléfono debe tener 10 dígitos.")
        return phone
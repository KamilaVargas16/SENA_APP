from django import forms
from .models import Programa


class ProgramaForm(forms.ModelForm):
    """Formulario basado en modelo para crear y editar programas de formación"""
    
    class Meta:
        model = Programa
        fields = [
            'codigo',
            'nombre',
            'nivel_formacion',
            'modalidad',
            'duracion_meses',
            'duracion_horas',
            'descripcion',
            'competencias',
            'perfil_egreso',
            'requisitos_ingreso',
            'centro_formacion',
            'regional',
            'estado',
            'fecha_creacion'
        ]
        # Widgets personalizados para mejorar la interfaz en el HTML
        widgets = {
            'codigo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: ADSI-2024-001'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre del programa'
            }),
            'nivel_formacion': forms.Select(attrs={
                'class': 'form-control'
            }),
            'modalidad': forms.Select(attrs={
                'class': 'form-control'
            }),
            'duracion_meses': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Duración en meses',
                'min': 1
            }),
            'duracion_horas': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Duración en horas',
                'min': 1
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción general del programa',
                'rows': 4
            }),
            'competencias': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Liste las competencias que desarrollará el aprendiz',
                'rows': 4
            }),
            'perfil_egreso': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describa el perfil del egresado',
                'rows': 4
            }),
            'requisitos_ingreso': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Liste los requisitos para ingresar al programa',
                'rows': 3
            }),
            'centro_formacion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del centro de formación'
            }),
            'regional': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Regional SENA'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-control'
            }),
            'fecha_creacion': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            })
        }
        # Etiquetas personalizadas
        labels = {
            'codigo': 'Código del Programa',
            'nombre': 'Nombre del Programa',
            'nivel_formacion': 'Nivel de Formación',
            'modalidad': 'Modalidad',
            'duracion_meses': 'Duración en Meses',
            'duracion_horas': 'Duración en Horas',
            'descripcion': 'Descripción del Programa',
            'competencias': 'Competencias a Desarrollar',
            'perfil_egreso': 'Perfil de Egreso',
            'requisitos_ingreso': 'Requisitos de Ingreso',
            'centro_formacion': 'Centro de Formación',
            'regional': 'Regional',
            'estado': 'Estado',
            'fecha_creacion': 'Fecha de Creación del Programa'
        }

    # Validaciones personalizadas
    
    def clean_codigo(self):
        """Validar formato del código del programa"""
        codigo = self.cleaned_data.get('codigo')
        if not codigo:
            raise forms.ValidationError("El código es obligatorio.")
        
        # Convertir a mayúsculas
        codigo = codigo.upper().strip()
        
        # Validar que no contenga caracteres especiales peligrosos
        if any(char in codigo for char in ['<', '>', '"', "'"]):
            raise forms.ValidationError("El código contiene caracteres no permitidos.")
        
        return codigo

    def clean_duracion_meses(self):
        """Validar que la duración en meses sea razonable"""
        duracion_meses = self.cleaned_data.get('duracion_meses')
        
        if duracion_meses and duracion_meses < 1:
            raise forms.ValidationError("La duración debe ser al menos 1 mes.")
        
        if duracion_meses and duracion_meses > 60:
            raise forms.ValidationError("La duración parece demasiado larga. Verifique el dato.")
        
        return duracion_meses
    
    def clean_duracion_horas(self):
        """Validar que la duración en horas sea razonable"""
        duracion_horas = self.cleaned_data.get('duracion_horas')
        
        if duracion_horas and duracion_horas < 40:
            raise forms.ValidationError("La duración debe ser al menos 40 horas.")
        
        if duracion_horas and duracion_horas > 10000:
            raise forms.ValidationError("La duración parece demasiado larga. Verifique el dato.")
        
        return duracion_horas
    
    def clean(self):
        """Validaciones que involucran múltiples campos"""
        cleaned_data = super().clean()
        duracion_meses = cleaned_data.get('duracion_meses')
        duracion_horas = cleaned_data.get('duracion_horas')
        
        # Validar coherencia entre meses y horas
        if duracion_meses and duracion_horas:
            # Aproximadamente 160 horas por mes (considerando 40 horas semanales)
            horas_estimadas = duracion_meses * 160
            
            # Verificar que la relación sea lógica (con un margen de +/- 50%)
            if duracion_horas > horas_estimadas * 2:
                self.add_error('duracion_horas', 
                    f"Las horas parecen muy altas para {duracion_meses} meses. Verifique.")
            elif duracion_horas < horas_estimadas * 0.25:
                self.add_error('duracion_horas', 
                    f"Las horas parecen muy bajas para {duracion_meses} meses. Verifique.")
        
        return cleaned_data
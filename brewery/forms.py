from django import forms

from .models import Batch


class BatchForm(forms.ModelForm):

    class Meta:
        model = Batch

        fields = (
            'name',
            'brew_date',
            'volume',
            'recipe',
            'notes',
        )

        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),

            'brew_date': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                }
            ),

            'volume': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                }
            ),

            'recipe': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 5,
                }
            ),

            'notes': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                }
            ),
        }

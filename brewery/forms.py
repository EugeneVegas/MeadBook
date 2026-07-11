from django import forms

from .models import Batch, Measurement


class DatePickerInput(forms.DateInput):
    input_type = 'date'


class DateTimePickerInput(forms.DateTimeInput):
    input_type = 'datetime-local'


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
            'brew_date': DatePickerInput(
                attrs={
                    'class': 'form-control',
                },
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')

        self.fields['recipe'].widget.attrs.update({
            'rows': 6,
        })

        self.fields['notes'].widget.attrs.update({
            'rows': 4,
        })


class MeasurementForm(forms.ModelForm):

    class Meta:
        model = Measurement

        fields = (
            'measured_at',
            'gravity',
            'temperature',
            'notes',
        )

        widgets = {
            'measured_at': DateTimePickerInput(
                attrs={
                    'class': 'form-control',
                },
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')

        self.fields['notes'].widget.attrs.update({
            'rows': 4,
        })

from django import forms

from .models import Batch, Measurement
from .utils.unit_conversion import sg_to_brix, brix_to_sg, brix_to_sg_corrected


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
    UNIT_CHOICES = (
        ('sg', 'SG'),
        ('brix', 'Brix'),
    )

    density = forms.DecimalField(
        label='Density',
        max_digits=5,
        decimal_places=3,
    )

    unit = forms.ChoiceField(
        label='Unit',
        choices=UNIT_CHOICES,
    )

    refractometer_correction = forms.BooleanField(
        label='Refractometer correction',
        required=False,
    )

    class Meta:
        model = Measurement

        fields = (
            'measured_at',
            'density',
            'unit',
            'refractometer_correction',
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
        self.batch = kwargs.pop('batch', None)

        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')

        self.fields['refractometer_correction'].widget.attrs.pop(
            'class',
            None,
        )
        self.fields['refractometer_correction'].widget.attrs[
            'class'
        ] = 'form-check-input'

        self.fields['notes'].widget.attrs.update({
            'rows': 4,
        })

    def clean(self):
        cleaned_data = super().clean()

        density = cleaned_data.get('density')
        unit = cleaned_data.get('unit')
        correction = cleaned_data.get('refractometer_correction')

        if density is None or unit is None:
            return cleaned_data

        if unit == 'sg':
            gravity = density

        elif unit == 'brix':
            gravity = self._brix_to_sg(
                density,
                correction=correction,
            )

        else:
            raise forms.ValidationError(
                'Unknown density unit.',
            )

        cleaned_data['gravity'] = gravity

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        instance.gravity = self.cleaned_data['gravity']

        if commit:
            instance.save()

        return instance

    def _brix_to_sg(self, brix, correction=False):
        if correction:
            if self.batch is None:
                raise forms.ValidationError(
                    'Batch is required for refractometer correction.',
                )

            original_gravity = self.batch.original_gravity

            if original_gravity is None:
                raise forms.ValidationError(
                    'Refractometer correction requires '
                    'original gravity.',
                )

            return brix_to_sg_corrected(
                sg_to_brix(original_gravity),
                brix,
            )

        return brix_to_sg(brix)

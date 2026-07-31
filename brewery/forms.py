from decimal import Decimal
from django import forms

from .models import Batch, Measurement
from .utils.unit_conversion import (
    brix_to_sg,
    brix_to_sg_corrected,
    sg_to_brix
)


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
        widget=forms.NumberInput(
            attrs={'placeholder': '0.000', 'step': '0.001'})
    )
    unit = forms.ChoiceField(
        label='Unit',
        choices=UNIT_CHOICES,
        widget=forms.Select()
    )

    class Meta:
        model = Measurement
        fields = (
            'measured_at',
            'density',
            'unit',
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

        if self.instance and self.instance.pk:
            self.fields['density'].initial = self.instance.gravity
            self.fields['unit'].initial = 'sg'

        # Стилизация Bootstrap
        for field_name, field in self.fields.items():
            if field_name == 'unit':
                field.widget.attrs.update({
                    'class': 'form-select-sm w-auto bg-white border-start-0',
                    'style': 'border-color: #dee2e6; '
                    'transition: border-color .15s ease-in-out, '
                    'box-shadow .15s ease-in-out;'
                })
            elif field_name == 'density':
                field.widget.attrs.update({
                    'class': 'form-control border-end-0'
                })
            else:
                field.widget.attrs.setdefault('class', 'form-control')

        self.fields['notes'].widget.attrs.update({'rows': 4})

    def clean(self):
        cleaned_data = super().clean()
        density = cleaned_data.get('density')
        unit = cleaned_data.get('unit')

        if density is None or unit is None:
            return cleaned_data

        if unit == 'sg':
            gravity = density
        elif unit == 'brix':
            gravity_float = self._brix_to_sg(float(density))
            gravity = Decimal(str(gravity_float))
        else:
            raise forms.ValidationError('Unknown density unit.')

        cleaned_data['gravity'] = gravity
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.gravity = self.cleaned_data['gravity']
        if commit:
            instance.save()
        return instance

    def _brix_to_sg(self, brix: float) -> float:
        # Автоматическая проверка: если батч передан
        # и у него ЕСТЬ начальная плотность (OG)
        if self.batch and self.batch.original_gravity:

            # Нюанс для режима редактирования:
            # если мы редактируем самый ПЕРВЫЙ замер (OG),
            # то коррекция алкоголя НЕ должна применяться,
            # ведь это начальное сусло!
            if self.instance and \
                    self.instance.pk == self.batch.earliest_measurement.pk:
                return brix_to_sg(brix)

            # Для всех последующих замеров (когда идет ферментация)
            # применяем формулу Новотного
            og_brix = sg_to_brix(float(self.batch.original_gravity))
            return brix_to_sg_corrected(og_brix, brix)

        # Если это самый первый замер в батче (Day 0),
        # алкоголя еще нет, просто конвертируем
        return brix_to_sg(brix)

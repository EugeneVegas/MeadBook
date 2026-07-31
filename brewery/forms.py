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

    class Meta:
        model = Measurement
        fields = (
            'measured_at',
            'raw_density',
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
            self.fields['raw_density'].initial = self.instance.raw_density
            self.fields['unit'].initial = self.instance.unit
        else:
            # Дефолтные плейсхолдеры для новых записей
            self.fields['raw_density'].widget.attrs.update(
                {'placeholder': '0.000', 'step': '0.001'})

        # Стилизация Bootstrap
        for field_name, field in self.fields.items():
            if field_name == 'unit':
                field.widget.attrs.update({
                    # Возвращаем form-select для правильных отступов и стрелочки
                    'class': 'form-select form-select-sm w-auto bg-white border-start-0',
                    'style': 'border-color: #dee2e6; '
                             'transition: border-color .15s ease-in-out, '
                             'box-shadow .15s ease-in-out;'
                })
            elif field_name == 'raw_density':
                field.widget.attrs.update({
                    'class': 'form-control border-end-0'
                })
            else:
                field.widget.attrs.setdefault('class', 'form-control')

        self.fields['notes'].widget.attrs.update({'rows': 4})

    def clean(self):
        cleaned_data = super().clean()
        raw_density = cleaned_data.get('raw_density')
        unit = cleaned_data.get('unit')

        if raw_density is None or unit is None:
            return cleaned_data

        if unit == 'sg':
            # Если ввели SG, то корректировать алкоголь не нужно
            gravity_float = float(raw_density)
        elif unit == 'brix':
            # Рассчитываем истинное SG по формуле Новотного
            gravity_float = self._brix_to_sg(float(raw_density))
        else:
            raise forms.ValidationError('Unknown density unit.')

        # Записываем вычисленное значение в cleaned_data для метода save()
        cleaned_data['gravity'] = Decimal(str(round(gravity_float, 3)))
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Переносим скрытое расчетное значение в модель перед записью
        instance.gravity = self.cleaned_data['gravity']
        if commit:
            instance.save()
        return instance

    def _brix_to_sg(self, brix: float) -> float:
        if self.batch and self.batch.original_gravity:
            # Если редактируем самый первый замер (OG),
            # то коррекция алкоголя не нужна
            if self.instance and self.instance.pk and \
                    self.batch.earliest_measurement and \
                    self.instance.pk == self.batch.earliest_measurement.pk:
                return brix_to_sg(brix)

            # Для всех последующих замеров применяем формулу Новотного
            og_brix = sg_to_brix(float(self.batch.original_gravity))
            return brix_to_sg_corrected(og_brix, brix)

        # Если это самый первый замер в батче, алкоголя еще нет
        return brix_to_sg(brix)

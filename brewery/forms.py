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
                attrs={'class': 'form-control'}
            ),
        }

    def __init__(self, *args, **kwargs):
        self.batch = kwargs.pop('batch', None)
        super().__init__(*args, **kwargs)

        # Если это новая запись, подкидываем дефолтный шаг
        if not self.instance or not self.instance.pk:
            self.fields['raw_density'].widget.attrs.update(
                {'placeholder': '0.000', 'step': '0.001'}
            )

        # Стилизация Bootstrap
        for field_name, field in self.fields.items():
            if field_name == 'unit':
                field.widget.attrs.update({
                    'class': 'form-select form-select-sm w-auto'
                    ' bg-white border-start-0',
                    'style': 'border-color: #dee2e6; '
                             'transition: border-color .15s ease-in-out, '
                             'box-shadow .15s ease-in-out;'
                })
            elif field_name == 'raw_density':
                field.widget.attrs.update(
                    {'class': 'form-control border-end-0'})
            else:
                field.widget.attrs.setdefault('class', 'form-control')

        self.fields['notes'].widget.attrs.update({'rows': 4})

    def clean(self):
        cleaned_data = super().clean()
        raw_density = cleaned_data.get('raw_density')
        unit = cleaned_data.get('unit')

        if raw_density is None or unit is None:
            return cleaned_data

        # Считаем чистое SG в зависимости от выбранного инструмента
        if unit == 'sg':
            gravity_float = float(raw_density)
        elif unit == 'brix':
            gravity_float = self._brix_to_sg(float(raw_density))
        else:
            raise forms.ValidationError('Unknown density unit.')

        cleaned_data['gravity'] = Decimal(str(round(gravity_float, 3)))
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.gravity = self.cleaned_data['gravity']
        if commit:
            instance.save()
        return instance

    def _brix_to_sg(self, brix: float) -> float:
        if self.batch:
            # Находим самый первый замер этого батча (наш священный OG)
            og_measurement = self.batch.measurements.order_by('id').first()

            # Если это самый первый замер в батче,
            # или мы редактируем его — алкоголя еще нет
            if not og_measurement \
                    or (self.instance
                        and self.instance.pk == og_measurement.pk):
                return brix_to_sg(brix)

            # Вытаскиваем чистый OG_Brix стартового сусла
            # без погрешностей перевода
            if og_measurement.unit == 'brix':
                og_brix = float(og_measurement.raw_density)
            else:
                og_brix = sg_to_brix(float(og_measurement.gravity))

            # Применяем формулу Новотного для бродящего сусла
            return brix_to_sg_corrected(og_brix, brix)

        return brix_to_sg(brix)

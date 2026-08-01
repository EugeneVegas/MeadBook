from datetime import date
from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from brewery.models import Batch, Measurement
from brewery.forms import MeasurementForm


class MeasurementFormTestCase(TestCase):

    def setUp(self):
        # 1. Создаем тестовый батч
        self.batch = Batch.objects.create(
            name="Automated Form Test Mead",
            brew_date=date(2026, 1, 1),
            volume=Decimal('10.0')
        )

        # 2. Создаем стартовый замер (Day 0) — это наш OG.
        # Заполняем новые обязательные поля raw_density и unit!
        self.og_measurement = Measurement.objects.create(
            batch=self.batch,
            measured_at=timezone.now() - timezone.timedelta(days=2),
            raw_density=Decimal('25.0'),  # Исходные 25 Brix
            unit='brix',
            # Чистая конвертация brix_to_sg(25) = 1.106
            gravity=Decimal('1.106'),
            temperature=Decimal('20.0')
        )

    def test_form_first_measurement_no_alcohol_correction(self):
        """Проверяем, что если создается первый замер (или правится OG),
        коррекция алкоголя НЕ применяется."""
        form_data = {
            'measured_at': timezone.now() - timezone.timedelta(days=2),
            'raw_density': Decimal('25.0'),
            'unit': 'brix',
            'temperature': Decimal('20.0'),
            'notes': 'Правим или создаем стартовый замер'
        }
        # Передаем инстанс нашего OG, как это делает UpdateView
        form = MeasurementForm(
            data=form_data, batch=self.batch, instance=self.og_measurement)

        self.assertTrue(form.is_valid())
        instance = form.save(commit=False)
        # Должна сработать чистая конвертация brix_to_sg, без Новотного = 1.106
        self.assertEqual(instance.gravity, Decimal('1.106'))

    def test_form_automatically_corrects_mid_fermentation_brix(self):
        """Проверяем, что форма сама понимает, что замер второй,
        и применяет формулу Новотного к Brix."""
        form_data = {
            'measured_at': timezone.now(),
            'raw_density': Decimal('15.0'),  # Вводим 15 Brix во время брожения
            'unit': 'brix',
            'temperature': Decimal('21.0'),
            'notes': 'Автоматическая коррекция без лишних галочек!'
        }

        form = MeasurementForm(data=form_data, batch=self.batch)

        self.assertTrue(form.is_valid())
        instance = form.save(commit=False)

        # ⚡ ПРОВЕРКА МАТЕМАТИКИ:
        # Для OG = 25 Brix и Current = 15 Brix формула Новотного выдает ровно 1.035 SG!
        self.assertEqual(instance.gravity, Decimal('1.035'))

    def test_form_edit_mode_blocks_recalculation_if_unchanged(self):
        """Проверяем, что если пользователь зашел в редактирование и не трогал плотность,
        вычисляемое поле gravity защищено от искажений и округлений."""
        # Создаем второй замер в базе (например, 15 brix -> 1.035 sg)
        mid_measurement = Measurement.objects.create(
            batch=self.batch,
            measured_at=timezone.now(),
            raw_density=Decimal('15.0'),
            unit='brix',
            gravity=Decimal('1.035'),
            temperature=Decimal('21.0')
        )

        form_data = {
            'measured_at': timezone.now(),
            'raw_density': Decimal('15.0'),  # Значение НЕ изменилось
            'unit': 'brix',
            'temperature': Decimal('21.0'),
            'notes': 'Я просто поменял текст заметки, плотность не трогал!'
        }

        # Инициализируем форму в режиме редактирования (UpdateView)
        form = MeasurementForm(
            data=form_data, batch=self.batch, instance=mid_measurement)

        self.assertTrue(form.is_valid())
        # Проверяем, что поле зафиксировалось как измененное по заметкам, но не по плотности
        self.assertNotIn('raw_density', form.changed_data)

        instance = form.save(commit=False)
        # Значение gravity должно остаться ровно таким, каким было в базе — 1.035
        self.assertEqual(instance.gravity, Decimal('1.035'))

from datetime import date
from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from brewery.models import Batch, Measurement
from brewery.forms import MeasurementForm


class MeasurementFormTestCase(TestCase):

    def setUp(self):
        self.batch = Batch.objects.create(
            name="Automated Form Test Mead",
            brew_date=date(2026, 1, 1),
            volume=Decimal('10.0')
        )
        # Создаем стартовый замер (Day 0) — это наш OG
        Measurement.objects.create(
            batch=self.batch,
            measured_at=timezone.now() - timezone.timedelta(days=2),
            gravity=Decimal('1.101'),  # 24 Brix
            temperature=Decimal('20.0')
        )

    def test_form_automatically_corrects_mid_fermentation_brix(self):
        """Проверяем, что форма САМА понимает, что замер второй,
            и применяет формулу Новотного."""
        form_data = {
            'measured_at': timezone.now(),
            'density': Decimal('18.0'),  # Пользователь просто вводит 18 Brix
            'unit': 'brix',
            'temperature': Decimal('21.0'),
            'notes': 'Автоматическая коррекция без лишних галочек!'
        }

        # Передаем батч, в котором уже ЕСТЬ сохраненный первый замер
        form = MeasurementForm(data=form_data, batch=self.batch)

        self.assertTrue(form.is_valid())
        instance = form.save(commit=False)

        # Форма автоматически определила наличие OG и скорректировала 18 Brix до 1.057 SG
        self.assertEqual(instance.gravity, Decimal('1.057'))

from datetime import date
from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from brewery.models import Batch, Measurement


class BatchModelPropertyTestCase(TestCase):
    """Проверяет корректность расчета свойств моделей Batch и Measurement."""

    def setUp(self):
        # Создаем тестовый батч
        self.batch = Batch.objects.create(
            name="Test Traditional Mead",
            brew_date=date(2026, 1, 1),
            volume=Decimal('10.0')
        )

    def test_batch_analytics_calculations(self):
        # 1. Стартовый замер (Day 0): 25.0 Brix (автоматически дает 1.106 SG)
        m1 = Measurement.objects.create(
            batch=self.batch,
            measured_at=timezone.now() - timezone.timedelta(days=5),
            raw_density=Decimal('25.0'),
            unit='brix',
            gravity=Decimal('1.106'),  # Исходное чистое SG
            temperature=Decimal('20.0')
        )

        # Проверяем базовые свойства батча на старте
        self.assertEqual(self.batch.original_gravity, Decimal('1.106'))
        self.assertEqual(self.batch.measurement_count, 1)

        # 2. Второй замер во время брожения: 15.0 Brix
        # По формуле Новотного (25.0 Brix OG -> 15.0 Brix Current)
        # дает ровно 1.035 SG
        m2 = Measurement.objects.create(
            batch=self.batch,
            measured_at=timezone.now(),
            raw_density=Decimal('15.0'),
            unit='brix',
            # Сохраняем уже скорректированное значение
            gravity=Decimal('1.035'),
            temperature=Decimal('21.5')
        )

        # Проверяем аналитические свойства модели Batch
        self.assertEqual(self.batch.current_gravity, Decimal('1.035'))
        self.assertEqual(self.batch.gravity_drop,
                         Decimal('0.071'))  # 1.106 - 1.035

        # Проверяем расчеты ABV и аттенюации, которые берут данные из utils
        self.assertTrue(self.batch.abv > Decimal('0.0'))
        self.assertTrue(self.batch.apparent_attenuation > Decimal('0.0'))

    def test_measurement_brix_property(self):
        """Проверяет динамическое свойство .brix у модели Measurement."""
        measurement = Measurement.objects.create(
            batch=self.batch,
            measured_at=timezone.now(),
            raw_density=Decimal('1.040'),
            unit='sg',
            gravity=Decimal('1.040'),
            temperature=Decimal('20.0')
        )
        # 1.040 SG это примерно 10.0 Brix (проверяем с точностью до 1 знака)
        self.assertAlmostEqual(float(measurement.brix), 10.0, places=1)

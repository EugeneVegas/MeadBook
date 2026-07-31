from datetime import date
from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from brewery.models import Batch, Measurement


class BatchModelPropertyTestCase(TestCase):
    """Verifies that model properties compute correct data from measurement stacks."""

    def setUp(self):
        # Set up a test batch
        self.batch = Batch.objects.create(
            name="Test Traditional Mead",
            brew_date=date(2026, 1, 1),
            volume=Decimal('10.0')
        )

    def test_batch_analytics_calculations(self):
        # 1. Day 0 Baseline: OG of 1.101 (roughly 24 Brix)
        m1 = Measurement.objects.create(
            batch=self.batch,
            measured_at=timezone.now() - timezone.timedelta(days=5),
            gravity=Decimal('1.101'),
            temperature=Decimal('20.0')
        )

        # Verify unfermented baseline metrics
        self.assertEqual(self.batch.original_gravity, Decimal('1.101'))
        self.assertEqual(self.batch.measurement_count, 1)

        # 2. Mid-Fermentation Check: Refractometer drops down to ~18 Brix
        # Based on your Novotny tests, 24 -> 18 Brix outputs 1.057 SG
        m2 = Measurement.objects.create(
            batch=self.batch,
            measured_at=timezone.now(),
            gravity=Decimal('1.057'),  # logged as calculated target
            temperature=Decimal('21.5')
        )

        # Trigger property evaluations
        self.assertTrue(self.batch.abv > Decimal('0.0'))
        self.assertTrue(self.batch.apparent_attenuation > Decimal('0.0'))

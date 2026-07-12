from django.db import models
from enum import StrEnum
from django.utils import timezone
from decimal import Decimal


class BatchStatus(StrEnum):
    NO_MEASUREMENTS = "⚪ No measurements"
    FERMENTING = "🟢 Fermenting"
    CONDITIONING = "🟡 Conditioning"


class Batch(models.Model):
    name = models.CharField(max_length=100)
    brew_date = models.DateField()
    volume = models.DecimalField(
        "Volume, l",
        max_digits=5,
        decimal_places=2,
    )
    recipe = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Batch'
        verbose_name_plural = 'Batches'
        ordering = ['-brew_date']

    def __str__(self) -> str:
        return self.name

    @property
    def measurement_count(self):
        return self.measurements.count()

    @property
    def latest_measurement(self):
        return self.measurements.first()

    @property
    def earliest_measurement(self):
        return self.measurements.last()

    @property
    def recent_measurements(self):
        return self.measurements.all()[:3]

    @property
    def current_gravity(self):
        measurement = self.latest_measurement
        if measurement is None:
            return None
        return measurement.gravity

    @property
    def original_gravity(self):
        measurement = self.earliest_measurement
        if measurement is None:
            return None
        return measurement.gravity

    @property
    def gravity_drop(self):
        og = self.original_gravity
        cg = self.current_gravity

        if og is None or cg is None:
            return None

        return og - cg

    @property
    def age_days(self):
        start_date = self.brew_date
        delta = timezone.localdate() - start_date

        return delta.days

    @property
    def status(self):
        if self.current_gravity is None:
            return BatchStatus.NO_MEASUREMENTS
        if self.current_gravity > Decimal('1.020'):
            return BatchStatus.FERMENTING
        return BatchStatus.CONDITIONING


class Measurement(models.Model):
    batch = models.ForeignKey(
        Batch,
        on_delete=models.CASCADE,
        related_name='measurements',
    )
    measured_at = models.DateTimeField()
    gravity = models.DecimalField(
        max_digits=5,
        decimal_places=3,
    )
    temperature = models.DecimalField(
        max_digits=3,
        decimal_places=1,
    )
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Measurement'
        verbose_name_plural = 'Measurements'
        ordering = ['-measured_at']

    def __str__(self):
        return (
            f'{self.batch.name}: '
            f'{self.gravity} '
            f'({self.measured_at:%d.%m.%Y})'
        )

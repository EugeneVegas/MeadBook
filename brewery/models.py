from django.db import models


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
    notes = models.TextField()

    class Meta:
        verbose_name = 'Measurement'
        verbose_name_plural = 'Measurements'
        ordering = ['-measured_at']

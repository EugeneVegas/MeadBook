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

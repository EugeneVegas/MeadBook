from django.db import models


class Batch(models.Model):
    class Meta:
        verbose_name = 'Batch'
        verbose_name_plural = 'Batches'
        ordering = ['-brew_date']

    name = models.CharField(max_length=100)
    brew_date = models.DateField()
    notes = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name

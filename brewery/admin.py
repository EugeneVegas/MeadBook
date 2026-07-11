from django.contrib import admin

from .models import Batch, Measurement


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'brew_date',
        'volume',
    )

    search_fields = (
        'name',
    )

    ordering = (
        '-brew_date',
    )


@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = (
        'measured_at',
        'gravity',
        'temperature',
        'notes'
    )

    ordering = (
        '-measured_at',
    )

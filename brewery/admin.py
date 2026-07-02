from django.contrib import admin

from .models import Batch


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

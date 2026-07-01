from django.shortcuts import render

from .models import Batch


def index(request):

    batches = Batch.objects.all()

    return render(
        request,
        'brewery/index.html',
        {
            'batches': batches,
        },
    )

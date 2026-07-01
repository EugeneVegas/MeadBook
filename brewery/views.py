from django.shortcuts import redirect, render

from .models import Batch

from .forms import BatchForm


def index(request):

    batches = Batch.objects.all()

    return render(
        request,
        'brewery/index.html',
        {
            'batches': batches,
        },
    )


def batch_create(request):

    if request.method == "POST":

        form = BatchForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("index")

    else:

        form = BatchForm()

    return render(
        request,
        "brewery/batch_form.html",
        {
            "form": form,
        },
    )

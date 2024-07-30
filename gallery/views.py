from django.shortcuts import render, redirect

from .forms import PhotoForm
#from blog.views import get_categories
from .models import Photo


# Create your views here.
def gallery(request):
    photos = Photo.objects.all()
    context = {'photos': photos}
    # context.update(get_categories())
    return render(request, "gallery/index.html", context)


def uploads(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('gallery')
    form = PhotoForm()
    return render(request, "gallery/upload.html", {'form': form})
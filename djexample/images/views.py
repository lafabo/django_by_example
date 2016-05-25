from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm
from django.shortcuts import get_object_or_404
from .models import Image


# Create your views here.
@login_required
def image_create(request):
	if request.method == 'POST':
		form = ImageCreateForm(data=request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			new_item = form.save(commit=False)
			# assign user to item
		new_item.user = request.user
		new_item.save()
		messages.success(request, 'Image saved')
		# redirect to new created item
		return redirect(new_item.get_absolute_url())
	else:
		# build form with data from bookmarklet via GET
		form = ImageCreateForm(data=request.GET)

	return render(request, 'images/image/create.html', {'section': 'images', 'form': form})


def image_detail(request, id, slug):
	image = get_object_or_404(Image, id=id, slug=slug)
	return render(request, 'images/image/detail.html', {'section': 'images', 'image': image})
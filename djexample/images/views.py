from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm
from django.shortcuts import get_object_or_404
from .models import Image
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from actions.utils import create_action
import redis
from django.conf import settings



# CONNECT TO REDIS
r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


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
			create_action(request.user, 'bookmarked image', new_item)
			messages.success(request, 'Image saved')
			# redirect to new created item
			return redirect(new_item.get_absolute_url())
	else:
		# build form with data from bookmarklet via GET
		form = ImageCreateForm(data=request.GET)

	return render(request, 'images/image/create.html', {'section': 'images', 'form': form})


def image_detail(request, id, slug):
	image = get_object_or_404(Image, id=id, slug=slug)
	# +1 to total images views
	total_views = r.incr('image:%s:views' % image.id)
	# + 1 to image_ranking
	r.zincrby('image_ranking', image.id, 1)
	return render(request, 'images/image/detail.html', {'section': 'images', 'image': image, 'total_views': total_views})


@ajax_required
@login_required
@require_POST
def image_like(request):
	image_id = request.POST.get('id')
	action = request.POST.get('action')
	if image_id and action:
		try:
			image = Image.objects.get(id=image_id)
			if action == 'like':
				image.users_like.add(request.user)
				create_action(request.user, 'likes', image)
			else:
				image.users_like.remove(request.user)
			return JsonResponse({'status': 'ok'})
		except:
			pass
	return JsonResponse({'status': 'ko'})


@login_required
def image_list(request):
	images = Image.objects.all()
	paginator = Paginator(images, 8)
	page = request.GET.get('page')
	try:
		images = paginator.page(page)
	except PageNotAnInteger:
		images = paginator.page(1)
	except EmptyPage:
		if request.is_ajax():
			# if request is ajax and page out of range return empty page
			return HttpResponse('')
		images = paginator.page(paginator.num_pages)
	if request.is_ajax():
		return render(request, 'images/image/list_ajax.html', {'section': 'images', 'images': images})
	return render(request, 'images/image/list.html', {'section': 'images', 'images': images})


@login_required
def image_ranking(request):
	image_ranking = r.zrange('image_ranking', 0, -1, desc=True)[:10]
	image_ranking_ids = [int(id) for id in image_ranking]

	most_viewed = list(Image.objects.filter(id__in=image_ranking_ids))
	most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id))

	return render(request, 'images/image/ranking.html', {'section': 'images', 'most_viewed': most_viewed})

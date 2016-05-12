from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm
from django.core.mail import send_mail
from .models import Comment
from .forms import CommentForm
from taggit.models import Tag


# Create your views here.
def post_list(request, tag_slug=None):
	object_list = Post.published.all()
	tag = None
	if tag_slug:
		tag = get_object_or_404(Tag, slug=tag_slug)
		object_list = object_list.filter(tags__in=[tag])


	paginator = Paginator(object_list, 5)   # 5 posts per page
	page = request.GET.get('page')
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)

	return render(request, 'blog/post/list.html', {'page': page,
	                                               'posts': posts,
	                                               'tag': tag})


def post_detail(request, year, month, day, post):
	post = get_object_or_404(Post, slug=post,
	                         status='published',
	                         publish__year=year,
	                         publish__month=month,
	                         publish__day=day)

	# list of active comments for this post
	comments = post.comments.filter(active=True)
	if request.method == 'POST':
		# a comment was posted
		comment_form = CommentForm(data=request.POST)
		if comment_form.is_valid():
			# create comment object, but don't save to database
			new_comment = comment_form.save(commit=False)
			new_comment.post = post
			new_comment.save()
	else:
		comment_form = CommentForm()

	return render(request, 'blog/post/detail.html', {'post': post,
	                                                 'comments': comments,
	                                                 'comment_form': comment_form})


class PostListView(ListView):
	queryset = Post.published.all()
	context_object_name = 'posts'
	paginate_by = 5
	template_name = 'blog/post/list.html'


def post_share(request, post_id):
	# get post by id
	post = get_object_or_404(Post, id=post_id, status='published')
	sent = False

	if request.method == 'POST':
		# form was submitted
		form = EmailPostForm(request.POST)
		if form.is_valid():
			# form fields passed
			cd = form.cleaned_data
			post_url = request.build_absolute_uri(post.get_absolute_url())
			subject = '%s (%s) recommends "%s"' % (cd['name'], cd['email'], post.title)
			message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])			# ... send e-mail
			send_mail(subject, message, 'admin@blog.com', [cd['to']])
			sent = True

	else:
		form = EmailPostForm()

	return render(request, 'blog/post/share.html', {'post': post,
	                                                'form': form,
	                                                'sent': sent})


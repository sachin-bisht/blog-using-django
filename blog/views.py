from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Comment, Like
from .forms import PostForm, CommentForm, SignupForm

from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

# Create your views here.
def post_list(request):

	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')

	return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
	
	post = get_object_or_404(Post, pk=pk)
	form = CommentForm()
	if request.method == "POST":
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.post = post
			comment.save()
			return redirect('post_detail', pk=post.pk)
		else:
			form = CommentForm()

	return render(request, 'blog/post_detail.html', {'post' : post, 'form' : form})

def post_new(request):
	if request.method == "POST":
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.now()
			post.save()
			return redirect('post_detail', pk=post.pk)

	else:
		form = PostForm()

	return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == "POST":
		form = PostForm(request.POST, instance=post)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.now()
			post.save()
			return redirect('post_detail', pk=post.pk)
	else:
		form = PostForm(instance=post)
	return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def comment_approve(request, pk):
	comment = get_object_or_404(Comment, pk=pk)
	comment.approve()
	return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
	comment = get_object_or_404(Comment, pk=pk)
	comment.delete()
	return redirect('post_detail', pk=comment.post.pk)

def signup(request):
	
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.save()
			current_site = get_current_site(request)
			mail_subject = 'Activate your blog account'
			message = render_to_string('blog/acc_active_email.html', {
				'user' : user,
				'domain' : current_site.domain,
				'uid' : urlsafe_base64_encode(force_bytes(user.pk)).decode(),
				'token' : account_activation_token.make_token(user),
				})
			to_email = form.cleaned_data.get('email')
			email = EmailMessage(
					mail_subject, message, to=[to_email]
			)
			email.send()
			return HttpResponse('Please Confirm your email address to complete registraion')
	else:
		form = SignupForm()	
	return render(request, 'blog/signup.html', {'form' : form})

def activate(request, uidb64, token):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None
	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.save()
		login(request, user)
		return HttpResponse('Thank you for your email confirmation.Now you can login your account')
	else:
		return HttpResponse('Activation link is invalid!')

def like_post(request):
	if request.method == 'GET':
		post_id = request.GET['post_id']
		likedpost = Post.objects.get(pk=post_id)
		m = Like(post=likedpost)
		m.save()
		return HttpResponse("Success!")
	else:
		return HttpResponse("Request method is not get")
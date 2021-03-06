from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
	path('', views.post_list, name='post_list'),
	path('post/<int:pk>/', views.post_detail, name='post_detail'),
	path('post/new/', views.post_new, name='post_new'),
	path('post/<int:pk>	/edit/', views.post_edit, name='post_edit'),
	url(r'^comment/(?P<pk>\d+)/approve/$', views.comment_approve, name='comment_approve'),
	url(r'^comment/(?P<pk>\d+)/remove/$', views.comment_remove, name='comment_remove'),
	url(r'^signup/$', views.signup, name='signup'),
	path('activate/<slug:uidb64>/<slug:token>', views.activate, name='activate'),
	url(r'^likepost/$', views.like_post, name='likepost'),
]
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^$', 'main.views.index'),
	url(r'^(.+)$', 'main.views.article'),
)

from django.conf.urls import patterns, include, url

from main.sitemaps import ArticleSitemap

urlpatterns = patterns('',
	(	r'^sitemap\.xml$',
		'django.contrib.sitemaps.views.sitemap',
		{
			'sitemaps': {
				'articles': ArticleSitemap,
			}
		}
	),
	url(r'^$', 'main.views.index'),
	url(r'^(contact)/$', 'main.views.contact'),
	url(r'^(.+)/$', 'main.views.article'),
)

from django.conf.urls import patterns, url

from pycard.sitemaps import ArticleSitemap

urlpatterns = patterns('',
    (    r'^sitemap\.xml$',
        'django.contrib.sitemaps.views.sitemap',
        {
            'sitemaps': {
                'articles': ArticleSitemap,
            }
        }
    ),
    url(r'^$', 'pycard.views.index'),
    url(r'^(contact)/$', 'pycard.views.contact'),
    url(r'^(.+)/$', 'pycard.views.article'),
)

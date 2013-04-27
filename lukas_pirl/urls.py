from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	# Examples:
	# url(r'^$', 'lukas_pirl.views.home', name='home'),
	# url(r'^lukas_pirl/', include('lukas_pirl.foo.urls')),

	url(r'^admin/', include(admin.site.urls)),
)

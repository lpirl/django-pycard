from urlparse import urlsplit

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.conf import settings

from main.models import Article

def get_article_or_404(slug):
	"""
	Shortcut to retrieve Articles
	"""
	return get_object_or_404(Article, slug=slug)

def slugs_from_request_path(request_path):
	"""
	Extracts a list of slugs from the request path.
	"""
	return filter(
		lambda s: bool(s),
		urlsplit(request_path)[2].split("/")
	)

def validate_slug_path_or_404(slug_path):
	"""
	Validates that request path equals parents slugs (recursively).
	"""
	parents = get_article_or_404(slug_path[-1]).parents()
	parents_slug_path = [a.slug for a in parents]

	if slug_path[:-1] != parents_slug_path:
		from django.http import Http404
		raise Http404('No article matches the given query.')

def index(request):
	return render(
		request,
		'index.html',
		{'vertically_center_menu': True}
	)

def article(request, request_path):
	slug_path = slugs_from_request_path(request_path)

	validate_slug_path_or_404(slug_path)

	return render(
		request,
		'article.html',
		{
			'article': get_article_or_404(slug_path[-1]),
		}
	)

def contact(request, slug):
	from main.forms import ContactForm

	form = ContactForm(data=request.POST or None)

	if form.is_valid():
		from django.core.mail import EmailMessage
		from django.contrib.sites.models import get_current_site

		sender_string = form.get_sender_string()

		email = EmailMessage(
			form.get_subject(get_current_site(request).name),
			form.cleaned_data['message'],
			to = ['"%s" <%s>' % (a[0], a[1]) for a in settings.MANAGERS],
			cc = [sender_string],
            headers = {
				'Reply-To': sender_string}
		)
		email.send()
		return HttpResponseRedirect('./message_sent')

	return render(
		request,
		'contact.html',
		{
			'form': form,
			'article': get_article_or_404(slug),
		}
	)

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.conf import settings

from main.models import Article

def index(request):
	return render(
		request,
		'index.html',
		{'vertically_center_menu': True}
	)

def article(request, slug):
	return render(
		request,
		'article.html',
		{
			'article': get_object_or_404(Article, slug=slug),
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
			'article': get_object_or_404(Article, slug=slug),
		}
	)


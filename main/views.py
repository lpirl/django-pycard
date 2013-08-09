from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect

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
		raise NotImplementedError
		return HttpResponseRedirect('.')

	return render(
		request,
		'contact.html',
		{
			'form': form,
			'article': get_object_or_404(Article, slug=slug),
		}
	)


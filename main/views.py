from django.shortcuts import render, get_object_or_404

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


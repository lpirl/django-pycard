from django.shortcuts import render

def index(request):
	return render(
		request,
		'index.html',
		{'vertically_center_menu': True}
	)


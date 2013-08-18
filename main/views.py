from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.conf import settings

from main.models import Article

def get_article_or_404(slug):
    """
    Shortcut to retrieve Articles
    """
    return get_object_or_404(Article, slug=slug)

def get_slug_list_from_request_path(request_path):
    """
    Extracts a list of slugs from the request path.
    """
    slugs = request_path.split("/")

    # Remove empty string and end of list (trailing slash in url)
    # both, with and without is valid, so we cannot rely on APPEND_SLASH
    if not slugs[-1]:
        slugs.pop()

    return slugs

def get_article_from_slug_list(slug_list):
    """
    Returns the corresponding article (last slug in slug list).

    Additionally, this function validates the path to the article.
    """
    try:
        requested_article = Article.objects.get(slug=slug_list[-1])
    except Article.DoesNotExist:
        return None

    # check if exactly all parents are present in slug list:
    if slug_list[:-1] != [a.slug for a in requested_article.parents()]:
        return None

    return requested_article

def index(request):
    return render(
        request,
        'index.html',
        {'vertically_center_menu': True}
    )

def article(request, request_path):
    slug_list = get_slug_list_from_request_path(request_path)

    requested_article = get_article_from_slug_list(slug_list)

    if not article:
        from django.http import Http404
        raise Http404('No article matches the given query.')

    return render(
        request,
        'article.html',
        {
            'article': requested_article,
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

from django.contrib.sitemaps import Sitemap
from pycard.models import Article

class ArticleSitemap(Sitemap):
    changefreq = "monthly"
    priority = 1

    def items(self):
        return filter(
            lambda a: a.needs_link(),
            Article.objects.filter(hide=False)
        )

    def lastmod(self, obj):
        return obj.date_modified

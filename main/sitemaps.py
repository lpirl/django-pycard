from django.contrib.sitemaps import Sitemap
from main.models import Article

class ArticleSitemap(Sitemap):
	changefreq = "monthly"
	priority = 1

	def items(self):
		return Article.objects.filter(hide=False)

	def lastmod(self, obj):
		return obj.date_modified

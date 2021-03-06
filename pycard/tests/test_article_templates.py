# encoding: utf-8

from django.test import TestCase

from pycard.models import Article

class ArticleTemplateTest(TestCase):
    """
    Tests for the display of an article
    """
    fixtures = ["test_article.json"]

    def test_subarticle_list_count(self):
        """
        Tests if sub articles lists are displayed accordingly
        """
        from itertools import product
        sub_articles_list_div = '<div class="sub_articles_list">'
        for top, bottom in product((True, False), repeat=2):
            article_qs = Article.objects.filter(
                    sub_articles_list_top=top
                ).filter(
                    sub_articles_list_bottom=bottom
                )
            self.assertTrue(
                article_qs.exists(),
                "No article with sub_article_list_top=%r and sub_article_list_bottom=%r found." % (top, bottom)
            )
            article = article_qs[0]
            response = self.client.get(article.get_absolute_url())
            self.assertContains(
                response,
                sub_articles_list_div,
                int(top) + int(bottom)
            )

    def test_subarticle_list_order(self):
        """
        Tests if sub articles lists are ordered correctly
        """
        parent = Article.objects.get(headline="Level 2 Article 1")
        children = parent.visible_sub_articles().order_by('-sort_priority')

        self.assertTrue(len(children)>1)

        self.assertNotEqual(    children[0].sort_priority,
                                children[1].sort_priority)

        # for readability (already implied)
        self.assertTrue(
            children[0].sort_priority
            >
            children[1].sort_priority
        )

        response_content = self.client.get(
            parent.get_absolute_url()
        ).content

        position_top = response_content.find(children[0].headline)
        position_bottom = response_content.find(children[1].headline)

        # make sure headlines were found
        self.assertNotEqual(position_top, -1)
        self.assertNotEqual(position_bottom, -1)

        self.assertTrue(position_top < position_bottom)

    def test_subarticle_list_links(self):
        """
        Tests if sub articles lists link to articles accordingly
        (ie: no link if article does not require it).
        """
        article = Article.objects.all().filter(
            headline='Level 1 Article 1')[0]

        child_with_link = None
        child_without_link = None
        for child in article.children.all():
            if child.needs_link() and not child.hide:
                child_with_link = child
            else:
                child_without_link = child

        self.assertIsNotNone(child_with_link)
        self.assertIsNotNone(child_without_link)

        response = self.client.get(article.get_absolute_url())

        self.assertContains(
            response,
            child_with_link.get_absolute_url()
        )
        self.assertNotContains(
            response,
            child_without_link.get_absolute_url()
        )

    def test_article_attachments(self):
        """
        Tests if articles attachments are displayed
        """
        article_qs = Article.objects.exclude(attachments=None)
        self.assertTrue(
            article_qs.exists(),
            "No article with attachments found."
        )
        article = article_qs[0]
        response = self.client.get(article.get_absolute_url())
        for attachment in article.attachments.all():
            self.assertContains(
                response,
                attachment.name
            )

    def test_article_content(self):
        """
        Tests if articles content is displayed
        """
        article = Article.objects.get(pk=12)
        self.assertNotEqual(article.content, "")
        response = self.client.get(article.get_absolute_url())

        self.assertContains(
            response,
            article.content
        )

    def test_article_headline(self):
        """
        Tests if articles headline is displayed
        """
        article = Article.objects.get(pk=12)
        self.assertNotEqual(article.headline, "")
        response = self.client.get(article.get_absolute_url())

        self.assertContains(
            response,
            article.headline,
            count=2 # html title & in content
        )

    def test_article_url(self):
        """
        Tests if articles headline is displayed
        """
        article_qs = Article.objects.filter(url__isnull=False)
        self.assertTrue(article_qs.exists())
        article = article_qs[0]
        response = self.client.get(article.get_absolute_url())

        self.assertContains(
            response,
            article.url
        )

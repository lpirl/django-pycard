# encoding: utf-8

from django.test import TestCase

from pycard.models import Article
from pycard.models import MenuItem
from pycard.models import Configuration
from pycard.templatetags.base_tags import menu as menu_context

class TagsTest(TestCase):
    """
    Tests for the templatetags module
    """
    fixtures = ["test_data/article.json", "test_data/configuration.json",
                "test_data/menu_items.json"]
    
    def setUp(self):
        self.response_index = self.client.get("/")

        self.response_visible_article = Article.objects.all(
            ).filter(hide=False).order_by("?")[0]
        self.response_visible = self.client.get(
            self.response_visible_article.get_absolute_url()
        )

        self.response_hidden_article = Article.objects.all(
            ).filter(hide=True).order_by("?")[0]
        self.response_hidden = self.client.get(
            self.response_hidden_article.get_absolute_url()
        )

        # shortcut:
        self.responses = (
            self.response_index,
            self.response_visible,
            self.response_hidden,
        )

    def test_squares(self):
        """
        Tests if there are enough squares :)
        """
        count = Configuration.get_int("squares_count")
        for response in self.responses:
            self.assertContains(
                response,
                '<div class="square background_square"',
                count=count
            )

    def test_menu_spacer(self):
        """
        Tests if menu spacer is [not] present on [not] /
        """
        spacer_div = '<div id="menu_spacer_vertically_center"></div>'
        self.assertContains(
            self.response_index,
            spacer_div,
            count=1
        )
        self.assertNotContains(
            self.response_visible,
            spacer_div,
        )

    def test_menu_items_existence(self):
        """
        Tests if all menu items are [not] present through corresponding
        tag.
        """
        items = MenuItem.objects.all()
        self.assertTrue(
            items.filter(root_article__hide=False).exists()
        )
        self.assertTrue(
            items.filter(root_article__hide=True).exists()
        )
        for response in (self.response_index, self.response_visible):
            for item in items:
                if item.root_article.hide:
                    self.assertNotContains(response,
                        item.root_article.headline)
                else:
                    self.assertContains(response,
                        item.root_article.headline)


    def test_menu_items_css_class(self):
        """
        Tests if all menu items are [not] present through corresponding
        tag.
        """
        menu_item = MenuItem.objects.filter(root_article__hide=False)[0]
        request_url = menu_item.root_article.get_absolute_url()
        response = self.client.get(request_url)

        import re
        response.content = re.sub('\s+', ' ', response.content)

        self.assertContains(
            response,
            'href="%s" class="square active"' % request_url,
            count=1
        )
        
    def test_menu_items_active_state(self):
        """
        Tests if the menu items that is closest to the current article
        (through the parent relation of articles) is marked as active.
        This is not done via the rendered HTML since it seems to be much
        more complicated and not ultimately beneficial.
        """
        menu_items = MenuItem.objects.filter(root_article__hide=False)
        self.assertTrue(menu_items.exists())
        menu_items_filter = menu_items.filter

        articles = Article.objects.all().filter(hide=False)
        self.assertTrue(articles.exists())

        for article in articles:
            parents = article.parents(True)

            # find menu item that points to the closest parent:
            closest_item_in_menu = None
            for parent in parents:
                candidate = menu_items_filter(root_article_id=parent)
                if candidate.exists():
                    closest_item_in_menu = candidate[0]

            if closest_item_in_menu:
                for item in menu_context(article)['items']:
                    self.assertEqual(
                        item.active,
                        int(item == closest_item_in_menu),
                        "For article %s, the attribute 'active' of menu item '%s' should be %u!" % (
                            str(article),
                            str(item),
                            int(item.root_article == closest_item_in_menu)
                        )
                    )

    def test_breadcrumbs(self):
        """
        Tests presence and correctness (roughly) of breadcrumbs in HTML.

        Quite primitive check but should be adequate for now.
        """
        crumb_parts = ['<div id="breadcrumbs">']
        add_crumb_part = crumb_parts.append
        for parent in self.response_visible_article.parents(True):
            add_crumb_part("&gt;")
            add_crumb_part("<a")
            add_crumb_part("href=\"%s\"" % parent.get_absolute_url())
            add_crumb_part("</a>")

        last_index = 0
        content_find = self.response_visible.content.find
        for part in crumb_parts:
            index = content_find(part, last_index)
            self.assertTrue(
                index > -1,
                "'%s' not found in response (search started at index %u)." % (
                part, last_index)
            )
            last_index = index

    def test_get_configuration_str(self):
        """
        Tests if string configurations are present through
        corresponding tag.
        """
        configuration_strings = (
            Configuration.objects.get(key="author").value,
            Configuration.objects.get(key="slogan").value
        )
        for string in configuration_strings:
            self.assertContains(
                self.response_index,
                string
            )

    def test_subarticle_list_hide(self):
        """
        Tests if hidden articles are hidden
        """
        hidden_qs = Article.objects.filter(hide=True).exclude(parent=None)
        self.assertTrue(hidden_qs.exists())
        hidden = hidden_qs[0]
        self.assertNotContains(
            self.client.get(hidden.parents()[-1].get_absolute_url()),
            hidden.headline
        )

    def test_subarticle_list(self):
        """
        Tests if sub articles are displayed
        """
        subarticle_qs = Article.objects.exclude(hide=True).exclude(
            parent=None)
        self.assertTrue(subarticle_qs.exists())
        article = subarticle_qs[0].parents()[-1]
        children = article.visible_sub_articles()

        self.assertTrue(children.exclude(url=None).exists())
        self.assertTrue(children.exclude(teaser=None).exists())
        self.assertTrue(children.exclude(headline=None).exists())

        response = self.client.get(article.get_absolute_url())
        for child in children:
            self.assertContains(response, child.url)
            self.assertContains(response, child.teaser)
            self.assertContains(response, child.headline)

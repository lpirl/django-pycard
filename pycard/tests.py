from django.conf import settings
from django.test import TestCase
from pycard.models import Article, Configuration, MenuItem
from pycard.forms import ContactForm

class ContactFormTest(TestCase):
    """
    Tests for the contact form
    """
    fixtures = ["test_data/contact.json"]
    
    def setUp(self):
        self.article = Article.objects.get(slug="contact")
        self.url = self.article.get_absolute_url()
        self.valid_data = {
            'name': "Regular John",
            'email': 'regular+tag@example.com',
            'subject': "I like cookies!",
            'message': "Dear Sir,\ncould you send me some cookies?\nJohn"
        }

    def test_valid_data_redirection(self):
        response = self.client.post(
            self.url,
            self.valid_data,
            follow=True
        )
        target_url = Article.objects.get(
            slug="message_sent"
        ).get_absolute_url()
        self.assertRedirects(response, target_url)

    def test_valid_data_email(self):
        from django.core import mail
        self.assertFalse(bool(mail.outbox))
        self.client.post(self.url, self.valid_data)
        self.assertTrue(len(mail.outbox) == 1)
        message = str(mail.outbox[0].message())
        for key, value in self.valid_data.items():
            for value_line in value.splitlines():
                self.assertTrue(
                    value_line in message,
                    "%s missing in email" % key
                )

    def test_injection(self):
        for field in ['name', 'subject']:
            self.valid_data[field] = "foo\nCc: me@example.com"
            response = self.client.post(
                self.url,
                self.valid_data
            )
            self.assertFormError(
                response,
                'form',
                'name',
                'Malicious data received.'
            )

    def test_get_sender_string(self):
        form = ContactForm(data=self.valid_data)
        self.assertTrue(form.is_valid())
        site_name = "mysite"
        parts = (settings.EMAIL_SUBJECT_PREFIX,
                 site_name,
                 self.valid_data['subject'])
        full_subject = form.get_subject(site_name)
        for part in parts:
            self.assertTrue(part in full_subject)

    def test_get_subject(self):
        variants = [
            {'name': 'me', 'email': ''},
            {'name': '', 'email': 'a@example.com'},
            {'name': 'me', 'email': 'a@example.com'},
            {'name': '', 'email': ''},
        ]
        data = self.valid_data
        for variant in variants:
            data.update(variant)
            form = ContactForm(data=data)
            self.assertTrue(form.is_valid())
            sender = form.get_sender_string()
            for value in variant.values():
                self.assertTrue(value in sender)

            if not ''.join(variant.values()):
                self.assertTrue("unknown" in sender)

class ArticleUrlTest(TestCase):
    """
    Tests for URLs pointing to articles.

    This sis somehow interesting because this app resolves some URLs
    itself.
    """
    fixtures = ["test_data/article.json"]
    
    def setUp(self):
        self.valid_url = "/level1_1/level2_1/level3_1/?query=foo#section"

    def test_valid_url(self):
        """
        Make sure valid URLs (get_absolute_url()) works
        """
        response = self.client.get(self.valid_url)
        self.assertTrue(Article.objects.get(slug="level2_1").hide)
        self.assertContains(response, "Level 3 Article 1")

    def assert_404_for_modified_valid_url(self, search, replace):
        """
        Shortcut for all checks expecting a 404 for a wrong URL
        """
        url = self.valid_url.replace(search, replace)
        response = self.client.get(url)
        self.assertEqual(
            response.status_code, 404,
            "'%s' returned not %d! (%d instead)" % (
                url, 404, response.status_code)
        )

    def test_missing_parent(self):
        """
        404 if not all parents are specified in the URL
        """
        self.assert_404_for_modified_valid_url("/level2_1", "")

    def test_no_parents(self):
        """
        404 if only the slug (w/o any parents) is specified in the URL
        """
        self.assert_404_for_modified_valid_url("/level1_1/level2_1", "")

    def test_wrong_parent(self):
        """
        404 if there is a not-parent (but existing article) in the URL
        """
        self.assert_404_for_modified_valid_url("level2_1", "level2_2")

class ArticleTemplateTest(TestCase):
    """
    Tests for the display of an article
    """
    fixtures = ["test_data/article.json"]

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
        Tests if articles attachments are displayed
        """
        article_qs = Article.objects.exclude(content="")
        self.assertTrue(
            article_qs.exists(),
            "No article with content found."
        )
        article = article_qs[0]
        response = self.client.get(article.get_absolute_url())
        self.assertContains(
            response,
            article.content
        )

class TagsTest(TestCase):
    """
    Tests for the templatetags module
    """
    fixtures = ["test_data/article.json", "test_data/configuration.json",
                "test_data/menu_items.json"]
    
    def setUp(self):
        self.response_index = self.client.get("/")
        self.response_not_index = self.client.get(
            Article.objects.all().order_by("?")[0].get_absolute_url()
        )

    def test_squares(self):
        """
        Tests if there are enough squares :)
        """
        count = Configuration.get_int("squares_count")
        for response in (self.response_index, self.response_not_index):
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
            self.response_not_index,
            spacer_div,
        )

    def test_menu_items(self):
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
        for response in (self.response_index, self.response_not_index):
            for item in items:
                if item.root_article.hide:
                    self.assertNotContains(response,
                        item.root_article.headline)
                else:
                    self.assertContains(response,
                        item.root_article.headline)

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

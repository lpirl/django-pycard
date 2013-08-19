from django.conf import settings
from django.test import TestCase
from main.models import Article, Configuration, MenuItem
from main.forms import ContactForm

class ContactFormTest(TestCase):
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
        response = self.client.post(self.url, self.valid_data)
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
    fixtures = ["test_data/article.json"]
    
    def setUp(self):
        self.valid_url = "/level1_1/level2_1/level3_1/?query=foo#section"

    def test_valid_url(self):
        response = self.client.get(self.valid_url)
        self.assertTrue(Article.objects.get(slug="level2_1").hide)
        self.assertContains(response, "Level 3 Article 1")

    def assert_404_for_modified_valid_url(self, search, replace):
        url = self.valid_url.replace(search, replace)
        response = self.client.get(url)
        self.assertEqual(
            response.status_code, 404,
            "'%s' returned not %d! (%d instead)" % (
                url, 404, response.status_code)
        )

    def test_missing_parent(self):
        self.assert_404_for_modified_valid_url("/level2_1", "")

    def test_no_parents(self):
        self.assert_404_for_modified_valid_url("/level1_1/level2_1", "")

    def test_wrong_parent(self):
        self.assert_404_for_modified_valid_url("level2_1", "level2_2")

class TagsTest(TestCase):
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

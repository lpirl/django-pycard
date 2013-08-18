from main.models import Article
from django.conf import settings
from django.test import TestCase
from main.forms import ContactForm

class ContactFormTest(TestCase):
    fixtures = ("contact.json", )
    
    def setUp(self):
        self.article = Article.objects.get(slug="contact")
        self.url = self.article.get_absolute_url()
        self.valid_data = {
            'name': "Regular John",
            'email': 'regular+tag@example.com',
            'subject': "I like cookies!",
            'message': "Dear Sir,\ncould you send me some cookies?\nJohn"
        }

    def test_valid_data(self):
        response = self.client.post(
            self.url,
            self.valid_data,
            follow=True
        )
        target_url = Article.objects.get(
            slug="message_sent"
        ).get_absolute_url()
        self.assertRedirects(response, target_url)

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

            if not ''.join(values):
                self.assertTrue("unknown" in sender)

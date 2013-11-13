# encoding: utf-8

from django.test import TestCase

from pycard.models import Article

class ArticleUrlTest(TestCase):
    """
    Tests for URLs pointing to articles.

    This sis somehow interesting because this app resolves some URLs
    itself.
    """
    fixtures = ["test_article.json"]
    
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

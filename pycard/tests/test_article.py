# encoding: utf-8

from django.test import TestCase

from pycard.models import Article

class ArticleTest(TestCase):
    """
    Tests for the model Article
    """
    fixtures = ["test_article.json"]

    def test_parents(self):
        """
        Make sure function returns parents in correct order.
        """
        # article pk's, root to leaf
        CORRECT_PATH_PKS = [7, 9, 11]
        CORRECT_PATH_ARTICLES = [
            Article.objects.get(pk=pk) for pk in CORRECT_PATH_PKS
        ]

        leaf_article = Article.objects.get(pk=11)

        self.assertEqual(
            CORRECT_PATH_ARTICLES[:-1],
            leaf_article.parents()
        )

        self.assertEqual(
            CORRECT_PATH_ARTICLES,
            leaf_article.parents(True)
        )

    def test_needs_link(self):
        """
        Should test needs_link(), BUT …

        … seems to be only testable with same code -> intentionally left
        blank so far.
        """
        pass

    def test_creation(self):
        """
        Tests creation of articles.

        This is useful because wrong default values (ex. lambdas) may
        break object creation.
        """
        a = Article()
        self.assertIsNone(a.pk)
        a.save()
        self.assertIsNotNone(a.pk)

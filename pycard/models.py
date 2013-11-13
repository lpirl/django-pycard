# encoding: utf-8
from os.path import basename
from decimal import Decimal
from django.db.models import (  Model, IntegerField, ForeignKey,
                                CharField, BooleanField, FileField,
                                ManyToManyField, TextField, URLField,
                                DateTimeField, DateField)

class Configuration(Model):
    """
    Holds global options.
    """
    key = CharField(    primary_key=True,
                        max_length=64,
                        null=False,
                        blank=False,
                        editable=True,
                        unique=True)
    value = CharField(max_length=64, blank=True)
    comment = TextField(blank=True)

    @staticmethod
    def get_str(key):
        return Configuration.objects.get_or_create(key=key)[0].value

    @staticmethod
    def get_int(key):
        return int(Configuration.get_str(key) or 0)

    @staticmethod
    def get_decimal(key):
        return Decimal(Configuration.get_str(key) or 0)

    def __unicode__(self):
        return unicode('%s : %s' % (self.key, self.value))

class MenuItem(Model):
    pos_x = IntegerField(null=False, blank=False, editable=True)
    pos_y = IntegerField(null=False, blank=False, editable=True)
    height = IntegerField(null=False, blank=False, editable=True)
    width = IntegerField(null=False, blank=False, editable=True)
    root_article = ForeignKey(    "Article", null=False, blank=False,
                                editable=True, related_name='+')
    def __unicode__(self):
        return unicode(self.root_article)

class Article(Model):

    # used for modification date in sitemap
    date_modified = DateTimeField(auto_now=True, editable=False)

    headline = CharField(null=False, blank=False, editable=True,
        max_length=128)

    slug = CharField(null=False, blank=False, editable=True,
        max_length=64, unique=True, help_text="Used in URL.")

    teaser = CharField(null=False, blank=True, editable=True,
                       max_length=1024)

    content = TextField(null=False, blank=True, editable=True)

    url = URLField(null=False, blank=True, editable=True)

    attachments = ManyToManyField("Attachment", blank=True,
        editable=True)

    content_media = ManyToManyField("ContentMedia", blank=True,
        editable=True, help_text="Resources referenced in content " +
        "(ex: images).")

    parent = ForeignKey("self", null=True, blank=True, editable=True,
        related_name='children', help_text="Article listed there.")

    sort_priority = IntegerField(null=True, blank=True, editable=True,
        default=0,
        help_text="Position in sub article list (highest = top).")

    sub_articles_list_top = BooleanField(editable=True, default=False)
    sub_articles_list_bottom = BooleanField(editable=True, default=True)
    hide = BooleanField(editable=True, help_text="Hides article in " +
        "lists but it will be still accessible.", default=False)

    class Meta:
        ordering = ['-sort_priority']

    def visible_sub_articles(self):
        """
        Returns a list of all sub articles (children) that not hidden.
        """
        return self.children.filter(hide=False)

    def parents(self, include_self=False):
        """
        Returns a list of all parents (recursively).

        ex. [root_parent, …, 2nd_parent, 1st_parent]
        """

        parents = []
        if include_self:
            parents.append(self)
        article = self
        while article.parent:
            parents.append(article.parent)
            article = article.parent
        parents.reverse()
        return parents

    def get_absolute_url(self):
        """
        Returns url to an article including the parents in the path.

        FIXME:    This is really not elegant. The must be a better way to deal
                with an arbitrary number of URL parts in Django.
        """
        from django.core.urlresolvers import reverse
        url_without_path = reverse("pycard.views.article", args=[self.slug])

        slug_path = self.parents() + [self]
        url_with_path = "/".join([a.slug for a in slug_path])

        return  url_without_path.replace(self.slug, url_with_path)

    def needs_link(self):
        """
        Method determines if the articles view needs to be linked.

        Ex, articles w/o any content or attachments or … do not need to
        be linked as a visit would be pointless.
        """
        if self.content:
            return True
        if self.attachments.all().exists():
            return True
        if self.content_media.all().exists():
            return True
        if self.children.all().exists():
            return True
        return False

    def __unicode__(self):
        if self.hide:
            return "(%s)" % unicode(self.headline)
        else:
            return unicode(self.headline)

class Attachment(Model):
    name = CharField(    null=False, blank=False, editable=True,
                        max_length=64)
    description = CharField(    null=False, blank=True, editable=True,
                                max_length=256)
    data = FileField(    blank=False, editable=True,
                        upload_to="attachments", max_length=256)

    def __unicode__(self):
        return unicode(self.__class__.name + basename(self.name))

class ContentMedia(Model):
    data = FileField(    blank=False, editable=True,
                        upload_to="content_media", max_length=256)

    def __unicode__(self):
        return unicode(self.__class__.name + basename(self.name))

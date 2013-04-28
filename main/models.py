from django.db.models import (	Model, IntegerField, ForeignKey,
								CharField, BooleanField, FileField,
								ManyToManyField, TextField, URLField)

class Configuration(Model):
	"""
	Holds global options.
	"""
	key = CharField(	primary_key=True,
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
	root_article = ForeignKey(	"Article", null=False, blank=False,
								editable=True, related_name='+')
	def __unicode__(self):
		return unicode(self.root_article)

	
class Article(Model):

	headline = CharField(	null=False, blank=False, editable=True,
							max_length=128)

	slug = CharField(	null=False, blank=False, editable=True,
						max_length=64)

	parent = ForeignKey(	"self", null=True, blank=True, editable=True,
							related_name='children')

	teaser = CharField(	null=False, blank=True, editable=True,
						max_length=256)

	content = TextField(null=False, blank=True, editable=True)

	url = URLField(	null=False, blank=True, editable=True)

	attachments = ManyToManyField(	"Attachment", blank=True,
									editable=True)

	sub_articles_list_top = BooleanField(editable=True)
	sub_articles_list_bottom = BooleanField(editable=True)
	hide = BooleanField(editable=True)

	def visible_sub_articles(self):
		return self.children.filter(hide=False)

	def __unicode__(self):
		if self.hide:
			return "(%s)" % unicode(self.headline)
		else:
			return unicode(self.headline)

class Attachment(Model):
	name = CharField(	null=False, blank=False, editable=True,
								max_length=64)
	description = CharField(	null=False, blank=True, editable=True,
								max_length=256)
	data = FileField(	blank=False, editable=True,
						upload_to="attachments", max_length=256)

	def __unicode__(self):
		return self.name

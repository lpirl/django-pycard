from django.db.models import (	Model, IntegerField, ForeignKey,
								CharField, BooleanField, FileField,
								ManyToManyField, TextField)

class Configuration(Model):
	"""
	Holds global options.
	"""
	option = CharField(	primary_key=True,
						max_length=64,
						null=False,
						blank=False,
						editable=True,
						unique=True)
	value = CharField(max_length=64, blank=True)
	comment = TextField(blank=True)

	@staticmethod
	def get_str(option):
		return Configuration.objects.get_or_create(option=option)[0].value

	@staticmethod
	def get_int(option):
		return int(Configuration.get_str(option) or 0)

	@staticmethod
	def get_decimal(option):
		return Decimal(Configuration.get_str(option) or 0)

	def __unicode__(self):
		return unicode('%s : %s' % (self.option, self.value))

class MenuItem(Model):
	pos_x = IntegerField(null=False, blank=False, editable=True)
	pos_y = IntegerField(null=False, blank=False, editable=True)
	height = IntegerField(null=False, blank=False, editable=True)
	width = IntegerField(null=False, blank=False, editable=True)
	root_article = ForeignKey(	"Article", null=False, blank=False,
								editable=True, related_name='+')

class Article(Model):

	headline = CharField(	null=False, blank=False, editable=True,
							max_length=128)

	slug = CharField(	null=False, blank=False, editable=True,
						max_length=64)

	teaser = CharField(	null=False, blank=True, editable=True,
						max_length=256)

	content = TextField(null=False, blank=True, editable=True)

	attachments = ManyToManyField(	"Attachment", blank=True,
									editable=True)

	sub_articles_list_top = BooleanField(editable=True)
	sub_articles_list_bottom = BooleanField(editable=True)
	hide = BooleanField(editable=True)

class Attachment(Model):
	name = CharField(	null=False, blank=False, editable=True,
								max_length=64)
	description = CharField(	null=False, blank=True, editable=True,
								max_length=256)
	data = FileField(	blank=False, editable=True,
						upload_to="attachments", max_length=256)

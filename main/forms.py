from django.forms import (	Form, CharField, EmailField, BooleanField,
							Textarea)

class ContactForm(Form):

	class Media:
		css = {
			'all': ('contact.css',)
		}
	
	name = CharField(required=False, max_length=63)
	email = EmailField(required=False)
	subject = CharField(required=False, max_length=127)
	message = CharField(max_length=65535, widget=Textarea)

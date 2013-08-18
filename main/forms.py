from django.forms import (    Form, CharField, EmailField, BooleanField,
                            Textarea, ValidationError)

class ContactForm(Form):

    class Media:
        css = {
            'all': ('contact.css',)
        }
    
    name = CharField(required=False, max_length=63)
    email = EmailField(required=False)
    subject = CharField(required=False, max_length=127)
    message = CharField(max_length=65535, widget=Textarea)

    def cleaned_data_for_header(self, key_in_cleaned_data):
        """
        This function is intended to prevent header injection.
        """

        data = self.cleaned_data[key_in_cleaned_data]

        if "\n" in data or "\r" in data:
            raise ValidationError("Malicious data received.")

        return     data

    def clean_name(self):
        return self.cleaned_data_for_header("name")

    def clean_subject(self):
        return self.cleaned_data_for_header("subject")

    def get_subject(self, site_name):
        from django.conf import settings

        return '%s[contact via %s] %s' % (
                settings.EMAIL_SUBJECT_PREFIX,
                site_name,
                self.cleaned_data['subject']
            )

    def get_sender_string(self):
        """
        Function assembles the email sender.

        Target format is: "Some One" <someone@example.com>
        Parts might be absent due to missing information.
        """

        data = self.cleaned_data
        out = []

        if data['name']:
            out.append('"%s"' % data['name'].replace("\"", "'"))

        if data['email']:
            out.append("<%s>" % data['email'])

        if out:
            return " ".join(out)
        else:
            return "unknown"

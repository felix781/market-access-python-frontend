import magic

from django import forms
from django.template.defaultfilters import filesizeformat


class MultipleValueField(forms.MultipleChoiceField):
    """
    Allows multiple values, but is not restricted to values in 'choices'
    """
    def valid_value(self, value):
        return True


class RestrictedFileField(forms.FileField):
    """
    Custom FileField with restrictions on content types and file size
    """
    mime_types = {
        'image/gif': '.gif',
        'image/png': '.png',
        'image/webp': '.webp',
        'image/jpeg': '.jpg',
        'text/csv': '.csv',
        'text/plain': '.txt',
        'application/rtf': '.rtf',
        'application/pdf': '.pdf',
        'application/msword': '.doc',
        'application/vnd.ms-excel': '.xls',
    }

    def __init__(self, *args, **kwargs):
        self.content_types = kwargs.pop("content_types")
        self.max_upload_size = kwargs.pop("max_upload_size")
        super().__init__(*args, **kwargs)

    def get_allowed_types(self):
        return [
            self.mime_types.get(content_type)
            for content_type in self.content_types
        ]

    def clean(self, *args, **kwargs):
        data = super().clean(*args, **kwargs)

        if not data:
            return

        content_type = magic.from_buffer(data.file.read(), mime=True)

        if content_type not in self.content_types:
            allowed_types = self.get_allowed_types()
            raise forms.ValidationError(
                f"Unsupported file format. The following file formats are "
                f"accepted {', '.join(allowed_types)}"
            )

        if data.size > self.max_upload_size:
            raise forms.ValidationError(
                f"File size exceeds the {filesizeformat(self.max_upload_size)}"
                " limit. Reduce file size and upload the document again."
            )

        return data
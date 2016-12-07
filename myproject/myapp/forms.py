# -*- coding: utf-8 -*-

from django import forms
from captcha.fields import CaptchaField


class DocumentForm(forms.Form):
    docfile = forms.FileField(label="")
    captcha = CaptchaField()
    
    def check_file_size(self):
        CONTENT_TYPES = ['image']
        MAX_UPLOAD_PHOTO_SIZE = 2097152
        content = self.cleaned_data['docfile']
        content_type = content.content_type.split('/')[0]
        if content_type in CONTENT_TYPES:
            if content._size > MAX_UPLOAD_PHOTO_SIZE:
                #msg = 'Keep your file size under 2 mb'
                #raise forms.ValidationError(msg)
                return "false"
            #if not content.name.endswith('.jpg'):
                #msg = 'Your file is not jpg'
                #raise forms.ValidationError(msg)
            else:
            #raise forms.ValidationError('File not supported')
                return "true"
    
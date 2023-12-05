from django import forms

class LinkForm(forms.Form):
    youtube_link = forms.URLField(label='YouTube Link')
    encryption_key = forms.CharField(max_length=20, required=False, label='Encryption Key')

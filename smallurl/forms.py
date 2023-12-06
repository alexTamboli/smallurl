from django import forms

class LinkForm(forms.Form):
    youtube_link = forms.URLField(label='YouTube Link')
    encryption_key = forms.CharField(max_length=128, required=False, label='Encryption Key')

class DecryptForm(forms.Form):
    encrypted_url = forms.CharField(max_length=255, label='Encrypted url')
    decryption_key = forms.CharField(max_length=255, label='Decryption Key')

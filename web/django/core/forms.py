from django import forms


class PromptForm(forms.Form):
    prompt = forms.CharField(label='Enter your prompt', max_length=500)


class TextInputForm(forms.Form):
    text = forms.CharField(
        label="Enter text to embed",
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 50}),
        max_length=1000
    )



import os
from django.core.exceptions import ValidationError
from .models import Document


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ("file",)

    def clean_file(self):
        upload = self.cleaned_data['file']
        ext = os.path.splitext(upload.name)[1].lower()
        if ext not in ('.txt', '.pdf'):
            raise ValidationError("Only .txt and .pdf files are allowed.")

        # Optional: check content_type
        ct = upload.content_type
        if ext == '.txt' and ct != 'text/plain':
            raise ValidationError("Invalid MIME type for .txt.")
        if ext == '.pdf' and ct != 'application/pdf':
            raise ValidationError("Invalid MIME type for .pdf.")

        return upload





class SearchForm(forms.Form):
    query = forms.CharField(
        label="Enter your query",
        max_length=512,
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 50,
        "placeholder": "What do you want to know?",
            "class": "form-control",}),
    )



class ChatMessageForm(forms.Form):
    message = forms.CharField(
        label="Your message",
        max_length=500,
        widget=forms.TextInput(attrs={
            "placeholder": "Type your message here…",
            "autocomplete": "off"
        })
    )

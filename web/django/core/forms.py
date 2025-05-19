from django import forms


class PromptForm(forms.Form):
    prompt = forms.CharField(label='Enter your prompt', max_length=500)


class TextInputForm(forms.Form):
    text = forms.CharField(
        label="Enter text to embed",
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 50}),
        max_length=1000
    )



from .models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model  = Document
        fields = ("file",)


class SearchForm(forms.Form):
    query = forms.CharField(
        label="Enter your query",
        max_length=512,
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 50,
        "placeholder": "What do you want to know?",
            "class": "form-control",}),
    )
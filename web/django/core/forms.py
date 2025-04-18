from django import forms


class PromptForm(forms.Form):
    prompt = forms.CharField(label='Enter your prompt', max_length=500)


class TextInputForm(forms.Form):
    text = forms.CharField(
        label="Enter text to embed",
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 50}),
        max_length=1000
    )
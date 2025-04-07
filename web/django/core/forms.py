from django import forms

class PromptForm(forms.Form):
    prompt = forms.CharField(label='Enter your prompt', max_length=500)

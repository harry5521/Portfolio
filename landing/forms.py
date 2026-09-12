from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Abu Huraira'
        })
    )
    
    email = forms.EmailField(
        max_length=100,
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'huraira@example.com'
        })
    )
    
    subject = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Project Discussion'
        })
    )
    
    message = forms.CharField(
        max_length=1000,
        widget=forms.Textarea(attrs={
            'class': 'form-input resize-none',
            'rows': 6,
            'placeholder': 'Tell me about your project or opportunity...'
        })
    )
    
    def clean_message(self):
        message = self.cleaned_data.get('message')
        if len(message) < 10:
            raise forms.ValidationError("Message must be at least 10 characters long.")
        return message
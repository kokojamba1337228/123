from django import forms
from .models import Property, Tag

class PropertyForm(forms.ModelForm):
    # Удаляем это поле, так как его обработка будет происходить напрямую в view
    # images = forms.FileField(
    #     widget=forms.FileInput(attrs={'multiple': True}), 
    #     required=False
    # )

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Property
        fields = ['title', 'description', 'price', 'location', 'size', 'tags'] 

class SupportMessageForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Ваш вопрос...',
        'rows': 4
    }), max_length=1000)
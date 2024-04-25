from django import forms
from inst_app.models import Publication, Follower, Comments
from django.forms import widgets


class PublicationForm(forms.ModelForm):

    class Meta:
        model = Publication
        fields = ('image', 'text')
        widgets = {
            'image': widgets.FileInput(attrs={
                'class': 'form-control mb-3 w-25',
            }),
            'text': widgets.Textarea(attrs={
                'class': 'form-control mb-3 w-25',
                'placeholder': 'Опишите ваше впечатление о фотографии здесь...'
            })
        }


class SearchForm(forms.Form):
    search = forms.CharField(max_length=20, required=False, label='Найти')


class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('publication', 'user', 'text')

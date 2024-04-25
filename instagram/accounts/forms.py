from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from accounts.models import Profile, GENDER_CHOICES
from django.core.validators import MinLengthValidator
from django.forms import widgets


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label='Email', required=True)

    avatar = forms.ImageField(label='Аватар', required=True)
    bio = forms.CharField(label='Информация о пользователе', max_length=150, required=False)
    phone_number = forms.CharField(label='Номер телефона', max_length=11, required=False,
                                   validators=[MinLengthValidator(11)])
    gender = forms.ChoiceField(label='Пол', choices=GENDER_CHOICES, initial='не указано', required=False)
    custom_gender = forms.CharField(label='Свой вариант пола', max_length=50, required=False)

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = (
            'username', 'password1',
            'password2', 'first_name',
            'last_name', 'email',
            'avatar', 'bio', 'phone_number',
            'gender', 'custom_gender'
        )


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email', 'username')
        widgets = {
            'first_name': widgets.TextInput(attrs={
                'class': 'form-control mb-3',
            }),
            'last_name': widgets.TextInput(attrs={
                'class': 'form-control mb-3',
            }),
            'email': widgets.EmailInput(attrs={
                'class': 'form-control mb-3',
            }),
            'username': widgets.TextInput(attrs={
                 'class': 'form-control mb-3',
            })
        }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('avatar', 'bio', 'phone_number')
        widgets = {
            'avatar': widgets.FileInput(attrs={
                'class': 'form-control mb-3',
            }),
            'bio': widgets.Textarea(attrs={
                'class': 'form-control mb-3',
                'type': 'text', 'style': 'height: 100px;'
            }),
            'phone_number': widgets.NumberInput(attrs={
                'class': 'form-control mb-3',
            }),
        }

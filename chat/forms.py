from .models import UserProfile
from django.forms import ModelForm, ImageField
from django.forms.widgets import FileInput


class UserProfileForm(ModelForm):
    avatar = ImageField(widget=FileInput)

    class Meta:
        model = UserProfile
        fields = ('avatar', )


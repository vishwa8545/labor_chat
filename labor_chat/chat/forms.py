from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, Organization,GroupChat

class UserProfileForm(UserCreationForm):
    """
    User registration  form for saving user profiles
    """

    first_name = forms.CharField(max_length="1000")
    last_name = forms.CharField(max_length="1000")
    Organization = forms.ModelChoiceField(queryset = Organization.objects.all() )
    avatar = forms.FileField(required=False)


class GroupChatForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(queryset=UserProfile.objects.all())


    class Meta:
        model = GroupChat
        fields = ['name']



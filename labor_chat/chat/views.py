from django.shortcuts import render,redirect
from django.db.models import Q
# Create your views here.
from django.views import View
from django.urls import reverse_lazy
from .models import UserProfile,Organization,GroupChat
from django.contrib.auth.models import User
from .forms import UserProfileForm,GroupChatForm

class CreateProfileView(View):
    """
    View class to create user profile
    form class:UserProfileForm,
    Model Class
    """
    form_class = UserProfileForm
    initial = {"key": "value"}
    template_name = "create_profile.html"

    def get(self,request):
        form = self.form_class(initial=self.initial)
        return render(request,'create_profile.html',{"form": form})


    def post(self,request):
        print("the data is",request)
        old_form = self.form_class(request.POST)
        if old_form.is_valid():
            print(old_form.cleaned_data,old_form.cleaned_data.get('password1'))
            user = User.objects.create(username=old_form.cleaned_data.get('username'),first_name=old_form.cleaned_data.get("first_name"),last_name=old_form.cleaned_data.get("last_name"))
            user.set_password(old_form.cleaned_data.get('password1'))
            user.save()
            profile = UserProfile.objects.create(user=user,organization=old_form.cleaned_data.get("Organization"))
            return redirect('login')
        else:
            print("the rrora",old_form.errors)
            form = self.form_class(initial=self.initial)
            return render(request, 'create_profile.html', {"form":old_form,"form_error":form})
class HomeView(View):
    """
    Home view class displayed to user after login
    here user will have options to create new chat group or go to any chat in his organization
    """
    def get(self,request):
        """
        get method to return home page
        """


        print(request.user)

        return render(request,'home.html',{})



class GroupChatCreateView(View):
    """
    View class to create  Group chats
    """
    form_class = GroupChatForm
    def get(self,request):
        form = GroupChatForm()

        return render(request, 'create_group_chat.html', {'form': form})
    def post(self,request):

        old_form = self.form_class(request.POST)
        print(old_form)
        if old_form.is_valid():
            old_form.cleaned_data.get('name')
            group = GroupChat.objects.create(name=old_form.cleaned_data.get('name'))
            members = old_form.cleaned_data.get('members')
            for member in members:
                group.members.add(member)

        else:
            form = self.form_class(initial=self.initial)
            return render(request, 'create_profile.html', {"form": old_form, "form_error": form})


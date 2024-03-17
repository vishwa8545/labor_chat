from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path('create_profile/', views.CreateProfileView.as_view(), name='create_profile'),
    path('chat_group_create/', login_required(views.GroupChatCreateView.as_view()), name='Grou-chat-create'),
    path('', login_required(views.HomeView.as_view()), name='Home-view'),
]
from django.urls.conf import path
from .views import (
    delete_cancel_invataion_friend_view,
    get_all_profiles_view,
    get_invites_view,
    get_invited_view,
    get_profile_view,
    invite_view,
    ProfileListView,
    get_friends_view,
    accept_view,
    ProfileDetailView
    )

app_name = 'profiles'

urlpatterns = [
    path('invites/', get_invites_view, name='invites'),
    path('invited/', get_invited_view, name='invited'),
    path('friends/', get_friends_view, name='friends'),
    path('invite/', invite_view, name='invite'),
    path('accept/', accept_view, name='accept'),
    path('delete/', delete_cancel_invataion_friend_view, name='delete'),
    path('profile/', get_profile_view, name='profile'),
    # path('<str:slug>/', get_profile_view, name='profile'),
    path('allprofiles/', ProfileListView.as_view(), name='allprofiles'),
    path('<slug>/', ProfileDetailView.as_view(), name='userprofile'),
    # path('allprofiles/', get_all_profiles_view, name='allprofiles'),
]
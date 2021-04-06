from django.shortcuts import redirect, render
from .models import Profile, Relationship
from .forms import ProfileForm
from django.views.generic import ListView, DetailView

from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
@login_required
def get_profile_view(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)
    confirm = False

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            confirm = True
    else:
        pass
    context = {
        'profile': profile,
        'form': form,
        'confirm': confirm
    }
    return render(request, "profiles/profile.html", context)

@login_required
def get_invites_view(request, ):
    profile = Profile.objects.get(user=request.user)
    qs = Relationship.objects.get_invites(profile)
    profiles = list(map(lambda x: x.sender, qs))
    isEmpty = False if qs else True
    context = {
        'qs': profiles,
        'isEmpty': isEmpty
    }
    return render(request, "profiles/invites.html", context)

@login_required
def get_invited_view(request, ):
    profile = Profile.objects.get(user=request.user)
    qs = Relationship.objects.get_invited(profile)
    profiles = list(map(lambda x: x.receiver, qs))
    if profiles:
        isEmpty = False
    else:
        isEmpty = True
    context = {
        'qs': profiles,
        'isEmpty': isEmpty
    }
    return render(request, "profiles/invited.html", context)

@login_required
def get_friends_view(request, ):
    profile = Profile.objects.get(user=request.user)
    qs = profile.get_friends()
    print(qs)
    context = {
        'qs': qs
    }
    return render(request, "profiles/invites.html", context)

@login_required
def get_all_profiles_view(request, ):
    user = request.user
    qs = Profile.objects.get_all_profiles(user)

    context = {
        'qs': qs
    }
    return render(request, "profiles/all_profiles.html", context)

class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = "profiles/profile_details.html"
    # context_object_name = 'qs'

    def get_object(self, slug=None):
        slug = self.kwargs.get('slug')
        profile = Profile.objects.get(slug=slug)
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # user = User.objects.get(username__iexact=self.request.user)
        # profile = Profile.objects.get(user=user)
        profile = Profile.objects.get(user=self.request.user)
        relationSenderProfile = Relationship.objects.filter(receiver=profile)
        relationReceiverProfile = Relationship.objects.filter(sender=profile)

        relationSenderUser = [relation.sender.user for relation in relationSenderProfile]
        relationReceiverUser = [relation.receiver.user for relation in relationReceiverProfile]

        context['relationSenderUser'] = relationSenderUser
        context['relationReceiverUser'] = relationReceiverUser
        context['posts'] = self.get_object().get_posts()
        context['therePosts'] = True if len(self.get_object().get_posts()) > 0 else False
        return context

class ProfileListView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = "profiles/all_profiles.html"
    context_object_name = 'qs'

    def get_queryset(self, ):
        qs = Profile.objects.get_all_profiles(self.request.user)
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # user = User.objects.get(username__iexact=self.request.user)
        # profile = Profile.objects.get(user=user)
        profile = Profile.objects.get(user=self.request.user)
        relationSenderProfile = Relationship.objects.filter(receiver=profile)
        relationReceiverProfile = Relationship.objects.filter(sender=profile)

        if len(self.get_queryset()) == 0 :
            context['isEmpty'] = True
        else:
            context['isEmpty'] = False

        relationSenderUser = [relation.sender.user for relation in relationSenderProfile]
        relationReceiverUser = [relation.receiver.user for relation in relationReceiverProfile]

        context['relationSenderUser'] = relationSenderUser
        context['relationReceiverUser'] = relationReceiverUser
        return context

@login_required    
def invite_view(request, ):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)
        if Relationship.objects.filter(sender=receiver, receiver=sender, status='send'):
            # relation = Relationship.objects.get(sender=receiver, receiver=sender, status='send')
            # relation.status = 'accepted'
            # relation.save()
            # print('here')
            pass
        else:
            relation = Relationship.objects.create(sender=sender, receiver=receiver, status='send')
        return redirect(request.META.get('HTTP_REFERER')) # REDIRECT TO THE DAME PAGE
    else:
        return redirect('profiles:profile')

@login_required
def accept_view(request, ):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        receiver = Profile.objects.get(user=user)
        sender = Profile.objects.get(pk=pk)
        if Relationship.objects.filter(sender=sender, receiver=receiver, status='send'):
            relation = Relationship.objects.get(sender=sender, receiver=receiver, status='send')
            relation.status = 'accepted'
            relation.save()

        return redirect(request.META.get('HTTP_REFERER')) # REDIRECT TO THE DAME PAGE
    else:
        return redirect('profiles:profile')

@login_required    
def delete_cancel_invataion_friend_view(request, ):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)
        if Relationship.objects.filter(
            (Q(sender=receiver) & Q(receiver=sender)) |
            (Q(sender=sender) & Q(receiver=receiver)) ):
            relation = Relationship.objects.filter(
            (Q(sender=receiver) & Q(receiver=sender)) |
            (Q(sender=sender) & Q(receiver=receiver)) )
            relation.delete()
        else:
            pass
        return redirect(request.META.get('HTTP_REFERER')) # REDIRECT TO THE DAME PAGE
    else:
        return redirect('profiles:profile')

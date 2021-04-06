from .models import Profile, Relationship

def profile_info(request, ):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        avatar = profile.avatar
        invitesCount = Relationship.objects.get_invites(receiver=profile).count()
        invitedCount = Relationship.objects.get_invited(sender=profile).count()
        return {
            'avatar':avatar,
            'invitesCount': invitesCount,
            'invitedCount': invitedCount,
        }
    return {}


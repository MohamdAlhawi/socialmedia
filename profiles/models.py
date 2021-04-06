from django.db.models.base import Model
# from posts.models import Reaction
from django.db import models
from django.contrib.auth.models import User
# from django.db.models.manager import RelatedManager
from .utils import get_random_code
from django.template.defaultfilters import slugify
from django.db.models import Q


# Create your models here.
STATUS_CHOICES = (
    ('send', 'send'),
    ('accepted', 'accepted')
)

class ProfileManager(models.Manager):

    def get_available_profiles(self, me):
        profiles = Profile.objects.all().exclude(user=me)
        profile = Profile.objects.get(user=me)
        qs = Relationship.objects.filter((Q(sender=profile) | Q(receiver=profile)))
        accepted = []
        for relation in qs:
            if relation.status == 'accepted':
                accepted.append(relation.receiver)
                accepted.append(relation.sender)
        available = [profile for profile in profiles if profile not in qs]
        return available

    def get_all_profiles(self, me):
        profiles = Profile.objects.all().exclude(user=me)
        return profiles

class Profile(models.Model):
    """Model definition for Profiles."""
    # TODO: Define fields here
    firstName = models.CharField( max_length=100)
    lastName = models.CharField(blank=True, max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default='no bio', max_length=300)
    email = models.EmailField(blank=True, max_length=254)
    country = models.CharField(blank=True, max_length=100)
    avatar = models.ImageField(upload_to='',blank=True,
     height_field=None, width_field=None, max_length=None, default='avatar.png')
    friends = models.ManyToManyField(User, 'relatedName', blank=True,)
    slug = models.SlugField(unique=True, blank=True)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    objects = ProfileManager()
    def get_friends(self):
        return self.friends.all()

    def get_friends_count(self):
        return self.friends.all().count()

    def get_posts(self):
        return self.posts.all()

    def get_posts_count(self):
        return self.posts.all().count()

    def get_given_reactions(self):
        reactions = self.reaction_set.all()
        total_reactions = 0
        for reaction in reactions:
            if reaction.value != 'Un':
                total_reactions += 1
        return total_reactions
    
    def get_recieved_reactions(self):
        posts = self.posts.all()
        total_reactions = 0
        for post in posts:
            total_reactions += post.reacted.all().count()
        return total_reactions

    def __str__(self):
        return f'{self.user.username}-{self.created.strftime("%d-%m-%Y")}'

    def save(self, *args, **kwagrs):
        if  self.slug == '':
            temp = False
            if self.firstName:
                if self.lastName:
                    toSlug = slugify(self.firstName + self.lastName)
                else:
                    toSlug = slugify(self.firstName)
                temp = Profile.objects.filter(slug=toSlug).exists()
                while temp:
                    toSlug = slugify(toSlug + get_random_code())
                    temp = Profile.objects.filter(slug=toSlug).exists()
            else:
                toSlug = slugify(self.user)#get_random_code()
            self.slug = toSlug
        super().save(*args, **kwagrs)

class RelationshipManager(models.Manager):
    """Model definition for RelationsManager  ."""

    # TODO: Define fields here
    def get_invites(self, receiver):
        qs = Relationship.objects.filter(receiver=receiver, status='send')
        return qs

    def get_invited(self, sender):
        qs = Relationship.objects.filter(sender=sender, status='send')
        return qs       

class Relationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(choices=STATUS_CHOICES, max_length=15)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    objects = RelationshipManager()
    def __str__(self):
        
        return f'{self.sender}-{self.receiver}-{self.status}'




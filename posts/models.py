from django.db import models
from django.core.validators import FileExtensionValidator
# from profiles.models import Profile
# import profiles.models

# Create your models here.

class Post(models.Model):
    """Model definition for Post."""

    # TODO: Define fields here
    content = models.TextField()
    image = models.ImageField(upload_to='posts', 
    validators=[FileExtensionValidator(['png', 'jpg', 'jpge'])],
    blank=True)
    reacted = models.ManyToManyField('profiles.Profile', default=None, related_name='reactions', blank=True)
    created = models.DateTimeField( auto_now=False, auto_now_add=True)
    updated = models.DateTimeField( auto_now=True, auto_now_add=False)
    author = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return str(self.author.slug+' '+self.content[:17]+'...')

    def num_reactions(self, ):
        return self.reacted.all().count()
    
    def get_friends(self):
        return self.friends.all()

    def get_friends_count(self):
        return self.friends.all().count()

    def get_friends(self):
        return self.friends.all()

    def get_friends_count(self):
        return self.friends.all().count()

    def num_comments(self):    
        return self.comment_set.all().count()

    class Meta:
        ordering = ('-created',)

class Comment(models.Model):
    """Model definition for Coment."""

    # TODO: Define fields here
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField( auto_now=False, auto_now_add=True)
    updated = models.DateTimeField( auto_now=True, auto_now_add=False)
    
    def __str__(self):
        return str(self.user.slug+' '+self.content[:17]+'...')

REACTION_TYPE = (
    ('like', 'like'), ('love', 'love'), ('haha', 'haha'), ('Un', 'Un')
)
class Reaction(models.Model):
    """Model definition for reation."""

    # TODO: Define fields here
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE)
    value = models.CharField(choices=REACTION_TYPE, max_length=10, default='Un')

    def __str__(self):
        return f'{self.user}-{self.post}-{self.value} '
# class PostReaction(models.Model):
#     """Model definition for reation."""

#     # TODO: Define fields here
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     user = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE)
#     value = models.CharField(choices=REACTION_TYPE, max_length=10, default='Un')

#     def __str__(self):
#         return f'{self.user}-{self.post}-{self.value} '


# class CommentReaction(models.Model):
#     """Model definition for reation."""

#     # TODO: Define fields here
#     comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
#     user = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE)
#     value = models.CharField(choices=REACTION_TYPE, max_length=10, default='Un')

#     def __str__(self):
#         return f'{self.user}-{self.post}-{self.value} '
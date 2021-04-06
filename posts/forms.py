from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    """Form definition for Post."""
    content = forms.CharField(widget=forms.Textarea(attrs={'rows':2}))
    class Meta:
        """Meta definition for Postform."""

        model = Post
        fields = ('content', 'image')
        
class CommentForm(forms.ModelForm):
    """Form definition for Comment."""
    content = forms.CharField(label='',
     widget=forms.Textarea(attrs={'rows':2, 'placeholder':'comment here'}))
    class Meta:
        """Meta definition for Commentform."""

        model = Comment
        fields = ('content',)


from django.core.checks import messages
from django.shortcuts import redirect, render
from .models import Post, Comment, Reaction
from profiles.models import Profile
from .forms import PostForm, CommentForm
from django.views.generic import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

@login_required
def post_comment_create_list_view(request, ):
    qs = Post.objects.all()
    profile = Profile.objects.get(user=request.user)

    postForm = PostForm()
    postAdded = False
    commentForm = CommentForm()

    if 'submit_postForm' in request.POST:
        postForm = PostForm(request.POST or None, request.FILES or None)
        if postForm.is_valid():
            instance = postForm.save(commit=False)
            instance.author = profile
            instance.save()
            postForm = PostForm()
            postAdded = True

    if 'submit_commentForm' in request.POST:
        commentForm = CommentForm(request.POST)
        if commentForm.is_valid():
            instance = commentForm.save(commit=False)
            instance.user = profile
            instance.post = Post.objects.get(id=request.POST.get('post_id'))
            instance.save()
            commentForm = CommentForm()

    context = {
        'qs': qs,
        'profile': profile,
        'postForm': postForm,
        'commentForm': commentForm,
        'postAdded': postAdded
    }
    return render(request, "posts/main.html", context)

def react_post(request, ):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)
        profile = Profile.objects.get(user=user)
        
        if profile in post_obj.reacted.all():
            post_obj.reacted.remove(profile)
            print('n')
        else:
            post_obj.reacted.add(profile)
            print('e')

        react, created= Reaction.objects.get_or_create(user=profile, post=post_obj)
        #  = False 
        if not created:
            if react.value == 'Un':
                react.vlaue = 'like'
                print('un')
            else:
                react.value = 'Un'
                print('like1')
        else:
                react.value = 'like'
                print('like2')
        react.save()
        post_obj.save()
    else:
        pass
    return redirect('posts:main-post-view')


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "posts/confirm_del.html"
    success_url = reverse_lazy('posts:main-post-view')

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        post = Post.objects.get(pk=pk)
        if not post.author.user == self.request.user:
            messages.Warning(self.request, 'not the author-delete permission denied')
        return post


class PostUpdateView(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = "posts/update.html"
    success_url = reverse_lazy('posts:main-post-view')

    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        if form.instance.author == profile:
            return super().form_valid(form)
        else:
            form.add_error(None, 'not the author-update permission denied')
            return super().form_invalid(form)


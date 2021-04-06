from django.urls.conf import path
from .views import post_comment_create_list_view, react_post, PostUpdateView, PostDeleteView

app_name = 'posts'

urlpatterns = [
    path('', post_comment_create_list_view, name='posts'),
    path('reacted/', react_post, name='reacted-post-view'),
    path('<pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('<pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
]
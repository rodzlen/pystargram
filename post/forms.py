from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory

from post.models import Post, PostImage, Comment
from util.forms import BootstrapModelForm


class PostForm(BootstrapModelForm):
    class Meta:
        model =Post
        fields = ('content',)

class PostImageForm(BootstrapModelForm):
    class Meta:
        model=PostImage
        fields = ('image',)

PostImageFormSet = inlineformset_factory(
    Post,PostImage,form=PostImageForm,extra=1,can_delete=True
)
formset = [
    PostImageForm(),PostImageForm(),PostImageForm(),
]

class CommentForm( BootstrapModelForm):
    class Meta:
        model= Comment
        fields = ('content',)
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView

from post.forms import PostForm, PostImageFormSet, CommentForm
from post.models import Post, Like


class PostListView(ListView):
    queryset = Post.objects.all().select_related('user').prefetch_related('images', 'comments','likes')
    template_name = 'post/list.html'
    paginate_by = 20
    ordering = '-create_at'

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)
        data['comment_form']= CommentForm()
        return data


class PostCreateView(LoginRequiredMixin,CreateView ):
    model= Post
    template_name = 'post/form.html'
    form_class = PostForm


    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['formset'] = PostImageFormSet()
        return data

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        image_formset = PostImageFormSet(self.request.POST, self.request.FILES, instance=self.object)
        if image_formset.is_valid():
            image_formset.save()
        return HttpResponseRedirect(reverse('main'))

class PostUpdateView(LoginRequiredMixin,UpdateView ):
    model= Post
    template_name = 'post/form.html'
    form_class = PostForm


    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['formset'] = PostImageFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        self.object = form.save()

        image_formset = PostImageFormSet(self.request.POST, self.request.FILES, instance=self.object)
        if image_formset.is_valid():
            image_formset.save()
        return HttpResponseRedirect(reverse('main'))

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)
@csrf_exempt
@login_required()
def toggle_like(request):
    post_pk = request.POST.get('post_pk')
    print(post_pk)
    if not post_pk:
        from django.http import Http404
        raise Http404()
    post = get_object_or_404(Post, pk=post_pk)
    user = request.user

    like, created = Like.objects.get_or_create(user=user, post=post)
    if not created:
        like.delete()
    from django.http import JsonResponse
    return JsonResponse({'created':created})
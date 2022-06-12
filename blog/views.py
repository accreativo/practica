from turtle import title
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View, UpdateView
from .forms import PostCreateForm
from .models import Post
from django.urls import reverse_lazy

# Create your views here.
class BlogListView(View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        context = {
            'posts':posts
        }
        return render(request, 'blog/index.html', context)

class BlogCreateView(View):
    def get(self, request, *args, **kwargs):
        formPostCreate = PostCreateForm()
        
        context = {
            'formPostCreate':formPostCreate
        }

        return render(request,'blog/create.html', context)

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            formPostCreate = PostCreateForm(request.POST)
            if formPostCreate.is_valid():
                title = formPostCreate.cleaned_data.get('title')
                content = formPostCreate.cleaned_data.get('content')

                p, created = Post.objects.get_or_create(title = title, content = content)
                p.save()

                return redirect('blog:home')

        context = {
            'formPostCreate':formPostCreate
        }

        return render(request,'blog/create.html', context)

class BlogDetailView(View):
    def get(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk = pk)
        context = {
            'post':post
        }
        return render(request, 'blog/detail.html', context)

class BlogUpdateView(UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/update.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('blog:detail', kwargs = {'pk':pk})
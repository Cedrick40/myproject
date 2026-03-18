from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import Post
from .forms import CommentForm
from django.shortcuts import redirect

class PostListView(ListView):
    model = Post
    template_name = "news/post_list.html"
    context_object_name = "posts"
    paginate_by = 6

    def get_queryset(self):
        queryset = Post.objects.all()

        search_query = self.request.GET.get("q")
        category = self.request.GET.get("category")

        if search_query:
            queryset = queryset.filter(title__icontains=search_query)

        if category:
            queryset = queryset.filter(category=category)

    # Get trending posts (same logic as context)
        trending = Post.objects.all()

        if search_query:
            trending = trending.filter(title__icontains=search_query)

        if category:
            trending = trending.filter(category=category)

        trending_ids = trending.order_by("-views").values_list("id", flat=True)[:3]

    # Exclude trending posts from main list
        queryset = queryset.exclude(id__in=trending_ids)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["search_query"] = self.request.GET.get("q", "")
        context["current_category"] = self.request.GET.get("category", "")

        context["categories"] = Post.objects.values_list("category", flat=True).distinct()
        search_query = self.request.GET.get("q")
        category = self.request.GET.get("category")

        trending = Post.objects.all()

        if search_query:
            trending = trending.filter(title__icontains=search_query)

        if category:
            trending = trending.filter(category=category)

        context["trending_posts"] = trending.order_by("-views")[:3]


        return context


class PostDetailView(DetailView):
    model = Post
    template_name = "news/post_detail.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        # Related posts (same category, excluding current post)
        context["related_posts"] = Post.objects.filter(
            category=self.object.category
        ).exclude(id=self.object.id)[:3]
        return context
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.save()

        return redirect("post_detail", pk=self.object.pk)

class CreatePostView(CreateView):
    model = Post
    fields = ["title", "content", "image", "category"]
    template_name = "news/create_post.html"
    success_url = reverse_lazy("post_list")
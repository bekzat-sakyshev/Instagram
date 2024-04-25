from urllib.parse import urlencode
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.views import generic
from accounts.models import Profile, User
from inst_app.forms import SearchForm
from inst_app.models import Publication, Follower, Like, Comments
from inst_app.forms import PublicationForm, CommentsForm
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexListView(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'users'
    model = User

    def get(self, request, *args, **kwargs):
        self.form = SearchForm(self.request.GET)
        self.search_value = None

        if self.form.is_valid():
            self.search_value = self.form.cleaned_data['search']

        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        if self.request.user.is_authenticated:
            followed_users = Follower.objects.filter(subscriber=self.request.user).values_list('followed', flat=True)
            context['posts'] = Publication.objects.filter(user__in=followed_users).order_by('-created_at')
            context['liked_publications'] = self.request.user.likes.values_list('publication_id', flat=True)
            context['comments'] = Comments.objects.all()
        else:
            context['posts'] = Publication.objects.all().order_by('-created_at')
        context['search_value'] = self.search_value

        if self.search_value:
            context['query_params'] = urlencode({'search': self.search_value})

        return context

    def get_queryset(self):
        qs = super().get_queryset()

        if self.search_value:
            query = (Q(username__icontains=self.search_value)
                     | Q(first_name__icontains=self.search_value)
                     | Q(email__icontains=self.search_value))

            qs = qs.filter(query).distinct()

        return qs


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Publication
    form_class = PublicationForm
    template_name = 'posts/post_create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.request.user.profile.publication_count += 1
        self.request.user.profile.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('index')


class PostDetailView(LoginRequiredMixin, generic.DetailView):
    model = Publication
    pk_url_kwarg = 'post_id'
    context_object_name = 'post'
    template_name = 'posts/detail.html'

    def get(self, request, *args, **kwargs):
        self.form = SearchForm(self.request.GET)
        self.search_value = None

        if self.form.is_valid():
            self.search_value = self.form.cleaned_data['search']

        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['search_value'] = self.search_value

        if self.search_value:
            users = User.objects.filter(
                Q(username__icontains=self.search_value) |
                Q(first_name__icontains=self.search_value) |
                Q(email__icontains=self.search_value)
            )
            context['users'] = users

        return context


class FollowCreateView(LoginRequiredMixin, generic.View):
    def post(self, request, *args, **kwargs):
        user = request.user
        followed_id = kwargs['id']
        follow_add = Follower(subscriber=user, followed_id=followed_id)
        follow_add.save()
        follower = get_object_or_404(Profile, user=followed_id)
        follower.followers_count += 1
        follower.save()
        user_profile = request.user.profile
        user_profile.following_count += 1
        user_profile.save()
        return redirect('profile', id=followed_id)


class FollowDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Follower
    pk_url_kwarg = 'id'

    def dispatch(self, request, *args, **kwargs):
        follow = self.get_object()
        follower = get_object_or_404(Profile, user=follow.followed)
        follower.followers_count -= 1
        follower.save()
        self.request.user.profile.following_count -= 1
        self.request.user.profile.save()
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        follow = self.get_object()
        return reverse('profile', kwargs={'id': follow.followed.id})


class PostLikeView(LoginRequiredMixin, generic.View):
    def post(self, request, *args, **kwargs):
        user = request.user
        publication_id = kwargs.get('post_id')

        existing_like = Like.objects.filter(user=user, publication_id=publication_id).first()
        if existing_like:
            existing_like.delete()

            publication = get_object_or_404(Publication, id=publication_id)
            publication.like -= 1
            publication.save()
        else:
            like = Like(user=user, publication_id=publication_id)
            like.save()

            publication = get_object_or_404(Publication, id=publication_id)
            publication.like += 1
            publication.save()

        return redirect('index')


class CommentCreateView(LoginRequiredMixin, generic.CreateView):
    model = Comments
    template_name = 'comment/create.html'
    form_class = CommentsForm

    def post(self, request, *args, **kwargs):
        user = request.user
        publication_id = kwargs.get('post_id')

        comment_text = request.POST.get('text')
        comment = Comments(user=user, publication_id=publication_id, text=comment_text)
        comment.save()

        publication = get_object_or_404(Publication, id=publication_id)
        publication.comment += 1
        publication.save()

        return redirect('index')

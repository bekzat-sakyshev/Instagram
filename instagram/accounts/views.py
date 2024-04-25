from django.contrib.auth import login, get_user_model, authenticate, views
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import generic
from accounts.forms import RegisterForm
from accounts.models import GENDER_CHOICES, Profile, User
from inst_app import models
from inst_app.forms import SearchForm
from accounts import forms
from django.contrib.auth.mixins import LoginRequiredMixin


def login_view(request):
    context = {}

    if request.method == 'GET':
        return render(request, 'auth/login.html', context=context)

    elif request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username_or_email)
            if user.check_password(password):
                user = authenticate(request, username=user.username, password=password)
                if user:
                    login(request, user)
                    return redirect('index')
        except User.DoesNotExist:
            pass

        try:
            user = User.objects.get(email=username_or_email)
            if user.check_password(password):
                user = authenticate(request, username=user.username, password=password)
                if user:
                    login(request, user)
                    return redirect('index')
        except User.DoesNotExist:
            pass

        context['has_errors'] = True
        context['error_message'] = \
            'Ошибка аутентификации. Пожалуйста, проверьте правильность введенных данных и попробуйте снова.'

    return render(request, 'auth/login.html', context=context)


class RegisterView(generic.CreateView):
    model = get_user_model()
    template_name = 'auth/register.html'
    form_class = RegisterForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gender_choices'] = GENDER_CHOICES
        return context

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()

        profile = Profile.objects.create(user=user)
        profile.avatar = form.cleaned_data['avatar']
        profile.bio = form.cleaned_data['bio']
        profile.phone_number = form.cleaned_data['phone_number']
        profile.gender = form.cleaned_data['gender']
        profile.custom_gender = form.cleaned_data['custom_gender']
        profile.save()

        login(self.request, user)

        return redirect(reverse('index'))


class UserDetailView(LoginRequiredMixin, generic.DetailView):
    model = get_user_model()
    template_name = 'auth/user_detail.html'
    context_object_name = 'user_profile'
    pk_url_kwarg = 'id'

    def get(self, request, *args, **kwargs):
        self.form = SearchForm(self.request.GET)
        self.search_value = None

        if self.form.is_valid():
            self.search_value = self.form.cleaned_data['search']

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        user = self.object
        current_user = self.request.user
        posts = models.Publication.objects.filter(user=user)
        followed = models.Follower.objects.filter(subscriber=current_user, followed=user).exists()
        follow_obj = models.Follower.objects.filter(subscriber=current_user, followed=user).first()
        users = None
        if self.search_value:
            users = User.objects.filter(
                Q(username__icontains=self.search_value) |
                Q(first_name__icontains=self.search_value) |
                Q(email__icontains=self.search_value)
            )

        return super().get_context_data(
            **kwargs,
            posts=posts,
            followed=followed,
            follow_obj=follow_obj,
            search_value=self.search_value,
            users=users
        )


class UserUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = get_user_model()
    form_class = forms.UserUpdateForm
    template_name = 'auth/user_update.html'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gender_choices'] = GENDER_CHOICES
        context['profile_form'] = self.get_profile_form()
        return context

    def get_profile_form(self):
        kwargs = {'instance': self.object.profile}

        if self.request.method == 'POST':
            kwargs['data'] = self.request.POST
            kwargs['files'] = self.request.FILES

        return forms.ProfileUpdateForm(**kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        user_form = self.get_form()
        profile_form = self.get_profile_form()

        if user_form.is_valid() and profile_form.is_valid():
            return self.form_valid(user_form, profile_form)

        return self.form_invalid(user_form, profile_form)

    def form_valid(self, user_form, profile_form):
        response = super().form_valid(user_form)
        profile_form.save()
        return response

    def form_invalid(self, user_form, profile_form):
        context = self.get_context_data(form=user_form, profile_form=profile_form)
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse('profile', kwargs={'id': self.object.id})

    def get_object(self, queryset=None):
        return self.request.user


class ChangePasswordView(LoginRequiredMixin, views.PasswordChangeView):
    template_name = 'auth/change_password.html'

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'id': self.request.user.id})


class UserListView(LoginRequiredMixin, generic.ListView):
    model = get_user_model()
    template_name = 'auth/users_list.html'
    context_object_name = 'users'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs.get('id')
        user = get_object_or_404(get_user_model(), id=user_id)

        if 'followers' in self.request.path:
            followers = models.Follower.objects.filter(followed=user)
            context['users'] = [i.subscriber for i in followers]
        elif 'subscriptions' in self.request.path:
            subscriptions = models.Follower.objects.filter(subscriber=user)
            context['users'] = [i.followed for i in subscriptions]
        else:
            context['users'] = []

        return context


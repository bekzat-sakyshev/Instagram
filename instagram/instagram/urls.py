"""instagram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from inst_app import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.IndexListView.as_view(), name='index'),
    path('accounts/', include('accounts.urls')),
    path('publication/add', views.PostCreateView.as_view(), name='post_add'),
    path('user/follow/<int:id>', views.FollowCreateView.as_view(), name='follow'),
    path('user/unfollow/<int:id>', views.FollowDeleteView.as_view(), name='unfollow'),
    path('publication/<int:post_id>/like', views.PostLikeView.as_view(), name='post_like'),
    path('publication/<int:post_id>/comment', views.CommentCreateView.as_view(), name='comment_add'),
    path('publication/detail/<int:post_id>/', views.PostDetailView.as_view(), name='post_detail')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

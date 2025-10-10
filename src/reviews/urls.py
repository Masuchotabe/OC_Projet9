from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from django.urls import path
from django.views.generic import RedirectView

from reviews import views

urlpatterns = [
                  path("", RedirectView.as_view(pattern_name='home', permanent=False)),
                  path("home/", views.HomeView.as_view(), name='home'),
                  path('tickets/create/', views.TicketCreateView.as_view(), name='ticket-create'),
                  path('tickets/<int:pk>/update/', views.TicketUpdateView.as_view(), name='ticket-update'),
                  path('tickets/<int:pk>/detail/', views.TicketDetailView.as_view(), name='ticket-detail'),
                  path('tickets/<int:pk>/delete/', views.TicketDeleteView.as_view(), name='ticket-delete'),

                  path('tickets/<int:ticket_id>/review/add/', views.ReviewCreateView.as_view(), name='review-create'),
                  path('review/create/', views.ReviewAndTicketCreateView.as_view(), name='review-and-ticket-create'),
                  path('review/<int:pk>/update/', views.ReviewUpdateView.as_view(), name='review-update'),
                  path('review/<int:pk>/delete/', views.ReviewDeleteView.as_view(), name='review-delete'),

                  path('user/posts', views.UserPostsView.as_view(), name='user-posts-list'),
                  path('user/follows', views.UserFollowView.as_view(), name='user-follow'),
                  path('user/userfollow/<int:user_follow_id>/delete', views.UserUnfollowView.as_view(),
                       name='user-unfollow')
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

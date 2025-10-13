from itertools import chain

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Value, CharField
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
    FormView,
    ListView,
)

from authentication.models import User
from reviews.forms import TicketForm, ReviewForm, UserFollowForm
from reviews.models import Ticket, Review, UserFollows


class HomeView(LoginRequiredMixin, ListView):
    """
    Displays the main feed for the logged-in user.
    Combines tickets and reviews from followed users and the user's own
    posts, then sorts them by creation date.
    """
    template_name = "reviews/home.html"

    def get_queryset(self):
        user = self.request.user
        tickets = user.get_viewable_tickets().annotate(
            content_type=Value("TICKET", CharField())
        )
        reviews = user.get_viewable_reviews().annotate(
            content_type=Value("REVIEW", CharField())
        )

        # Merge the two querysets into a single sorted list
        posts = sorted(
            chain(reviews, tickets), key=lambda post: post.time_created, reverse=True
        )
        return posts


class UserPostsView(LoginRequiredMixin, ListView):
    """
    Displays a list of all posts (tickets and reviews) created by the
    logged-in user.
    """
    template_name = "reviews/user/posts_list.html"

    def get_queryset(self):
        user: User = self.request.user
        tickets = user.tickets.all().annotate(content_type=Value("TICKET", CharField()))
        reviews = user.reviews.all().annotate(content_type=Value("REVIEW", CharField()))

        # Merge the two querysets into a single sorted list
        posts = sorted(
            chain(reviews, tickets), key=lambda post: post.time_created, reverse=True
        )
        return posts


class TicketCreateView(LoginRequiredMixin, CreateView):
    """Displays a form to create a new ticket."""
    model = Ticket
    form_class = TicketForm
    template_name_suffix = "/form"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TicketUpdateView(LoginRequiredMixin, UpdateView):
    """Displays a form to edit an existing ticket."""
    model = Ticket
    form_class = TicketForm
    template_name_suffix = "/form"
    success_url = reverse_lazy("home")


class TicketDetailView(LoginRequiredMixin, DetailView):
    """Displays the details of a specific ticket."""
    model = Ticket
    template_name_suffix = "/detail"


class TicketDeleteView(LoginRequiredMixin, DeleteView):
    """Displays a confirmation page to delete a ticket."""
    model = Ticket
    success_url = reverse_lazy("user-posts-list")
    template_name_suffix = "/confirm_delete"


class ReviewAndTicketCreateView(LoginRequiredMixin, CreateView):
    """Displays a form to create a ticket and a review simultaneously."""
    model = Review
    form_class = ReviewForm
    template_name_suffix = "/extended_form"
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ticket_form"] = TicketForm()
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        ticket_form = TicketForm(self.request.POST, self.request.FILES)
        ticket_form.instance.user = self.request.user
        if ticket_form.is_valid():
            ticket = ticket_form.save()
            form.instance.ticket = ticket
        return super().form_valid(form)


class ReviewCreateView(LoginRequiredMixin, CreateView):
    """Displays a form to create a review in response to an existing ticket."""
    model = Review
    form_class = ReviewForm
    template_name_suffix = "/form"
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ticket_id = self.kwargs.get("ticket_id")
        if ticket_id:
            ticket = Ticket.objects.get(id=ticket_id)
            context["ticket"] = ticket
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        ticket_id = self.kwargs.get("ticket_id")
        if ticket_id:
            form.instance.ticket_id = ticket_id
        return super().form_valid(form)


class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    """Displays a form to edit an existing review."""
    model = Review
    form_class = ReviewForm
    template_name_suffix = "/form"
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ticket_id = self.kwargs.get("ticket_id")
        if ticket_id:
            ticket = Ticket.objects.get(id=ticket_id)
            context["ticket"] = ticket
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        ticket_id = self.kwargs.get("ticket_id")
        if ticket_id:
            form.instance.ticket_id = ticket_id
        return super().form_valid(form)


class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    """Displays a confirmation page to delete a review."""
    model = Review
    success_url = reverse_lazy("user-posts-list")
    template_name_suffix = "/confirm_delete"


class UserFollowView(LoginRequiredMixin, FormView):
    """
    Manages the "Subscriptions" page.
    Displays a form to follow new users, as well as lists of followed users
    and followers.
    """
    form_class = UserFollowForm
    success_url = reverse_lazy("user-follow")
    template_name = "reviews/user/follow_form.html"

    def form_valid(self, form):
        user = self.request.user
        username = form.cleaned_data["username"]
        user_to_follow = User.objects.get_by_natural_key(username)
        # Create the follow relationship
        UserFollows.objects.create(user=user, followed_user=user_to_follow)
        return HttpResponseRedirect(self.get_success_url())


class UserUnfollowView(LoginRequiredMixin, View):
    """Handles the logic for unfollowing a user."""

    def post(self, request, user_follow_id, *args, **kwargs):
        user = self.request.user
        user.following.get(id=user_follow_id).delete()
        return HttpResponseRedirect(reverse("user-follow"))

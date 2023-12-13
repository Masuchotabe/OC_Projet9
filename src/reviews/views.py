from itertools import chain

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Value, CharField
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, FormView

from authentication.models import User
from reviews.forms import TicketForm, ReviewForm, UserFollowForm
from reviews.models import Ticket, Review, UserFollows


def home(request):
    user = request.user
    tickets = user.get_viewable_tickets()
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    reviews = user.get_viewable_reviews()
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

    posts = sorted(
        chain(reviews, tickets), key=lambda post: post.time_created, reverse=True
    )
    return render(request, "reviews/home.html", locals())


class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    form_class = TicketForm
    template_name_suffix = "/form"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TicketUpdateView(LoginRequiredMixin, UpdateView):
    model = Ticket
    form_class = TicketForm
    template_name_suffix = "/form"
    success_url = reverse_lazy("home")


class TicketDetailView(LoginRequiredMixin, DetailView):
    model = Ticket
    template_name_suffix = "/detail"


class TicketDeleteView(LoginRequiredMixin, DeleteView):
    model = Ticket
    success_url = reverse_lazy("home")


class ReviewAndTicketCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name_suffix = "/extended_form"
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ticket_form'] = TicketForm()
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
    model = Review
    form_class = ReviewForm
    template_name_suffix = "/form"
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ticket_id = self.kwargs.get('ticket_id')
        if ticket_id:
            ticket = Ticket.objects.get(id=ticket_id)
            context['ticket'] = ticket
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        ticket_id = self.kwargs.get('ticket_id')
        if ticket_id:
            form.instance.ticket_id = ticket_id
        return super().form_valid(form)


class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name_suffix = "/form"
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ticket_id = self.kwargs.get('ticket_id')
        if ticket_id:
            ticket = Ticket.objects.get(id=ticket_id)
            context['ticket'] = ticket
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        ticket_id = self.kwargs.get('ticket_id')
        if ticket_id:
            form.instance.ticket_id = ticket_id
        return super().form_valid(form)


class UserFollowView(LoginRequiredMixin, FormView):
    form_class = UserFollowForm
    success_url = reverse_lazy("user-follow")
    template_name = "reviews/user/follow_form.html"

    def form_valid(self, form):
        user = self.request.user
        username = form.cleaned_data["username"]
        user_to_follow = User.objects.get_by_natural_key(username)
        UserFollows.objects.create(user=user, followed_user=user_to_follow)
        return HttpResponseRedirect(self.get_success_url())


class UserUnfollowView(LoginRequiredMixin, View):

    def post(self, request, user_follow_id, *args, **kwargs):
        user = self.request.user
        user.following.get(id=user_follow_id).delete()
        return HttpResponseRedirect(reverse("user-follow"))

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, FormView

from authentication.models import User
from reviews.forms import TicketForm, ReviewForm, UserFollowForm
from reviews.models import Ticket, Review


# Create your views here.

def home(request):
    posts = Ticket.objects.all()
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


class UserFollowView(FormView):
    form_class = UserFollowForm
    success_url = reverse_lazy("user-follow")  # TODO A MODIFIER
    template_name = "reviews/user/follow_form.html"

    def form_valid(self, form):
        username = form.cleaned_data["username"]
        user_to_follow = User.objects.get_by_natural_key(username)
        return HttpResponseRedirect(self.get_success_url())

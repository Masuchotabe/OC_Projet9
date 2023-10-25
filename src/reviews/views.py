from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView

from reviews.forms import TicketForm
from reviews.models import Ticket


# Create your views here.

def home(request):
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


class TicketDeleteView(LoginRequiredMixin, DeleteView):
    model = Ticket
    success_url = reverse_lazy("home")


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    form_class = TicketForm
    template_name_suffix = "/form"
    success_url = reverse_lazy("home")

    def get_initial(self):
        # Récupérez le ticket à partir de l'URL
        ticket_id = self.kwargs.get('ticket_id')
        if ticket_id:
            return {'ticket': ticket_id}
        return {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ticket_id = self.kwargs.get('ticket_id')
        if ticket_id:
            ticket = Ticket.objects.get(id='ticket_id')
            print(ticket)
            context['ticket'] = ticket
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

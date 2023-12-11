from django.contrib.auth.models import AbstractUser
from django.db.models import Q

from reviews.models import Ticket, Review


class User(AbstractUser):
    first_name = None
    last_name = None

    REQUIRED_FIELDS = []

    def get_viewable_tickets(self):
        users = [user_follow.followed_user for user_follow in self.following.all()]
        users.append(self)
        tickets = Ticket.objects.filter(user__in=users)
        return tickets

    def get_viewable_reviews(self):
        users = [user_follow.followed_user for user_follow in self.following.all()]
        users.append(self)
        query = Q(user__in=users) | (Q(ticket__user=self) & ~Q(user__in=users))
        reviews = Review.objects.filter(query).distinct()
        return reviews

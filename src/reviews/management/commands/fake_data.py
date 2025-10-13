from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from reviews.models import Ticket, Review, UserFollows, UserBlocked
from faker import Faker
import random
import requests

User = get_user_model()


class Command(BaseCommand):
    help = "Populate database with test data for tickets, reviews, follows and blocks"

    def add_arguments(self, parser):
        parser.add_argument(
            "--users", type=int, default=20, help="Number of users to create"
        )
        parser.add_argument(
            "--tickets", type=int, default=50, help="Number of tickets to create"
        )
        parser.add_argument(
            "--reviews", type=int, default=80, help="Number of reviews to create"
        )
        parser.add_argument(
            "--with-images", action="store_true", help="Add images to tickets (slower)"
        )

    def get_random_image(self):
        """Télécharge une image aléatoire depuis Lorem Picsum"""
        try:
            # Dimensions aléatoires entre 400x300 et 800x600
            width = random.randint(400, 800)
            height = random.randint(300, 600)
            url = f"https://picsum.photos/{width}/{height}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return ContentFile(
                    response.content, name=f"ticket_{random.randint(1000, 9999)}.jpg"
                )
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"Failed to download image: {e}"))
        return None

    def handle(self, *args, **options):
        fake = Faker("fr_FR")

        self.stdout.write("Clearing existing data...")
        User.objects.all().delete()

        # 1. Créer les administrateurs
        self.stdout.write("Creating admin users...")
        admins = []
        admin1 = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="admin123"
        )
        admins.append(admin1)

        admin2 = User.objects.create_superuser(
            username="superadmin", email="superadmin@example.com", password="admin123"
        )
        admins.append(admin2)

        # 2. Créer les utilisateurs normaux
        self.stdout.write("Creating regular users...")
        users = []
        for i in range(options["users"]):
            user = User.objects.create_user(
                username=fake.user_name() + str(i),
                email=fake.email(),
                password="password123",
            )
            users.append(user)

        # Combiner tous les users (admins + users normaux) pour les relations
        all_users = admins + users

        # 3. Créer les relations de suivi (follows)
        self.stdout.write("Creating user follows...")
        follows_created = 0
        for user in all_users:
            # Chaque user suit entre 1 et 7 autres users
            num_follows = random.randint(1, min(7, len(all_users) - 1))
            potential_follows = [u for u in all_users if u != user]
            users_to_follow = random.sample(potential_follows, num_follows)

            for followed_user in users_to_follow:
                try:
                    UserFollows.objects.create(user=user, followed_user=followed_user)
                    follows_created += 1
                except Exception:
                    # En cas de doublon (ne devrait pas arriver avec unique_together)
                    pass

        # 4. Créer quelques relations de blocage (blocks)
        self.stdout.write("Creating user blocks...")
        blocks_created = 0
        # Environ 10% des users bloquent quelqu'un
        users_who_block = random.sample(all_users, k=max(1, len(all_users) // 10))
        for user in users_who_block:
            # Bloquer 1 à 3 personnes
            num_blocks = random.randint(1, min(3, len(all_users) - 1))
            potential_blocks = [u for u in all_users if u != user]
            users_to_block = random.sample(potential_blocks, num_blocks)

            for blocked_user in users_to_block:
                try:
                    UserBlocked.objects.create(user=user, blocked_user=blocked_user)
                    blocks_created += 1
                except Exception:
                    pass

        # 5. Créer les tickets
        self.stdout.write("Creating tickets...")
        if options["with_images"]:
            self.stdout.write(
                self.style.WARNING("Images enabled - this may take a while...")
            )

        tickets = []
        for i in range(options["tickets"]):
            image = None
            # 60% des tickets ont une image si l'option est activée
            if options["with_images"] and random.random() < 0.6:
                image = self.get_random_image()

            ticket = Ticket.objects.create(
                title=fake.catch_phrase()[:128],
                description=fake.paragraph(nb_sentences=random.randint(3, 8))[:2048],
                user=random.choice(all_users),
                image=image,
            )
            tickets.append(ticket)

            if (i + 1) % 10 == 0:
                self.stdout.write(f"  Created {i + 1}/{options['tickets']} tickets...")

        # 6. Créer les reviews
        self.stdout.write("Creating reviews...")
        reviews_created = 0

        # 70% des reviews sont associées à des tickets existants
        num_reviews_with_tickets = int(options["reviews"] * 0.7)

        for i in range(num_reviews_with_tickets):
            ticket = random.choice(tickets)

            # Un user ne peut pas reviewer son propre ticket
            available_users = [u for u in all_users if u != ticket.user]

            if available_users:
                # Vérifier qu'il n'y a pas déjà une review de cet user sur ce ticket
                reviewer = random.choice(available_users)

                # Éviter les doublons (un user peut faire une seule review par ticket)
                if not Review.objects.filter(ticket=ticket, user=reviewer).exists():
                    Review.objects.create(
                        ticket=ticket,
                        rating=random.randint(0, 5),
                        headline=fake.sentence(nb_words=random.randint(4, 10))[:128],
                        body=fake.paragraph(nb_sentences=random.randint(5, 15))[:8192],
                        user=reviewer,
                    )
                    reviews_created += 1

        # 30% des reviews sont créées avec leur propre ticket (ticket+review par le même user)
        num_reviews_with_own_tickets = options["reviews"] - num_reviews_with_tickets

        self.stdout.write("Creating ticket+review combos...")
        for i in range(num_reviews_with_own_tickets):
            # Créer un ticket
            user = random.choice(all_users)

            image = None
            # 60% des tickets ont une image si l'option est activée
            if options["with_images"] and random.random() < 0.6:
                image = self.get_random_image()

            ticket = Ticket.objects.create(
                title=fake.catch_phrase()[:128],
                description=fake.paragraph(nb_sentences=random.randint(3, 8))[:2048],
                user=user,
                image=image,
            )
            tickets.append(ticket)

            # Créer une review par le même user
            Review.objects.create(
                ticket=ticket,
                rating=random.randint(0, 5),
                headline=fake.sentence(nb_words=random.randint(4, 10))[:128],
                body=fake.paragraph(nb_sentences=random.randint(5, 15))[:8192],
                user=user,
            )
            reviews_created += 1

        # 7. Statistiques finales
        tickets_with_images = Ticket.objects.exclude(image="").count()

        self.stdout.write(
            self.style.SUCCESS(
                f"\n✅ Database populated successfully!\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"👥 Users:          {User.objects.count()} ({len(admins)} admins, {len(users)} regular)\n"
                f"🎫 Tickets:        {Ticket.objects.count()} ({tickets_with_images} with images)\n"
                f"⭐ Reviews:        {Review.objects.count()}\n"
                f"👣 Follows:        {UserFollows.objects.count()}\n"
                f"🚫 Blocks:         {UserBlocked.objects.count()}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"🔑 Admin credentials:\n"
                f"   Username: admin | Password: admin123\n"
                f"   Username: superadmin | Password: admin123\n"
                f"\n💡 Regular user credentials:\n"
                f"   Username: {users[0].username} | Password: password123\n"
            )
        )

        # Afficher quelques stats intéressantes
        user_with_most_tickets = max(all_users, key=lambda u: u.tickets.count())
        user_with_most_reviews = max(all_users, key=lambda u: u.reviews.count())
        user_with_most_follows = max(all_users, key=lambda u: u.following.count())

        self.stdout.write(
            f"📊 Fun stats:\n"
            f"   Most tickets: {user_with_most_tickets.username} ({user_with_most_tickets.tickets.count()})\n"
            f"   Most reviews: {user_with_most_reviews.username} ({user_with_most_reviews.reviews.count()})\n"
            f"   Most follows: {user_with_most_follows.username} ({user_with_most_follows.following.count()})\n"
        )

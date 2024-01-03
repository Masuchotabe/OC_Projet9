from crispy_forms.bootstrap import InlineRadios, FieldWithButtons
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from django import forms
from django.core.exceptions import ValidationError
from django.forms import RadioSelect, Textarea, CharField
from django.utils.translation import gettext as _

from authentication.models import User
from reviews.models import Ticket, Review


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', "image"]
        widgets = {
            "description": Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'TicketForm'
        self.helper.form_method = 'post'
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'title',
            'description',
            'image',
        )


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['headline', 'rating', "body"]
        widgets = {
            "body": Textarea(attrs={"rows": 3}),
            "rating": RadioSelect(choices=[(i, i) for i in range(6)])
        }
        labels = {
            'headline': "Titre",
            'rating': "Note",
            'body': "Commentaire"
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'ReviewForm'
        self.helper.form_method = 'post'
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'headline',
            InlineRadios('rating'),
            'body',
        )


class UserFollowForm(forms.Form):
    username = CharField(max_length=150, label="Nom d'utilisateur")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'FollowForm'
        self.helper.form_method = 'post'
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            FieldWithButtons(Field('username', placeholder="Nom d'utilisateur", aria_label="Nom d'utilisateur"),
                             Submit('submit', 'Suivre')
                             ),
        )

    def clean_username(self):
        data = self.cleaned_data["username"]
        if not User.objects.filter(username=data).exists():
            raise ValidationError(_("Ce nom d'utilisateur n'existe pas."), code='bad_username')
        return data

from crispy_forms.bootstrap import InlineRadios
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, HTML
from django import forms
from django.forms import RadioSelect

from reviews.models import Ticket, Review


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', "image"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'TicketForm'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'title',
            'description',
            'image',
            Div(
                HTML(
                    """<a class="btn btn-secondary m-2" href="{% url 'home' %}">
                    Annuler
                    </a>"""),
                Submit('submit', 'Enregistrer', css_class="m-2"),
                css_class="d-flex justify-content-center"
            )
        )


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['headline', 'rating', "body"]
        widgets = {
            "rating": RadioSelect(choices=[(i, i) for i in range(5)])
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'ReviewForm'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'headline',
            'body',
            InlineRadios('rating'),
            Div(
                HTML(
                    """<a class="btn btn-secondary m-2" href="{% url 'home' %}">
                    Annuler
                    </a>"""),
                Submit('submit', 'Enregistrer', css_class="mx-auto"),
                css_class="d-flex justify-content-center"
            )
        )

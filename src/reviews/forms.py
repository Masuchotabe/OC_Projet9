from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from reviews.models import Ticket


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', "image"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'TicketForm'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Enregistrer'))


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', "image"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'ReviewForm'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Enregistrer'))

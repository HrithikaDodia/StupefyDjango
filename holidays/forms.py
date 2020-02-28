from django.forms import ModelForm
from .models import *
from django.forms.models import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from .custom_layout_object import *

class FlightPersonForm(ModelForm):

    class Meta:
        model = FlightPerson
        exclude = ()

FlightPersonFormSet = inlineformset_factory(
    FlightBooking, FlightPerson, form=FlightPersonForm,
    fields=['firstname', 'lastname', 'seat_no', 'row_no'], extra=1, can_delete=True
    )

class FlightBookingForm(ModelForm):

    class Meta:
        model = FlightBooking
        exclude = ['user','flight' ]

    def __init__(self, *args, **kwargs):
        super(FlightBookingForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3 create-label'
        self.helper.field_class = 'col-md-9'
        self.helper.layout = Layout(
            Div(
                Fieldset('Add titles',
                    Formset('titles')),
                HTML("<br>"),
                ButtonHolder(Submit('submit', 'save')),
                )
            )
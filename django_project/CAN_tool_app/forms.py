from django.contrib.auth.forms import AuthenticationForm
from django.forms import Form, CharField, IntegerField, ModelChoiceField, ChoiceField, FileField
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from .models import Signal
from django.forms import widgets


class AuthForm(AuthenticationForm):
    username = CharField(
        widget=widgets.TextInput(attrs={
            'class': "form-control",
        }))
    password = CharField(
        widget=widgets.PasswordInput(attrs={
            'class': "form-control",
        }))


class CarForm(Form):
    name = CharField(
        max_length=64,
        widget=widgets.TextInput(attrs={
            'class': "form-control",
        }))
    year = IntegerField(
        validators=[MinValueValidator(2000), MaxValueValidator(3000)],
        widget=widgets.NumberInput(attrs={
            'class': "form-control",
        }))
    note = CharField(
        max_length=255,
        required=False,
        widget=widgets.TextInput(attrs={
            'class': "form-control",
        }))


class CanBusForm(Form):
    name = CharField(
        max_length=64,
        widget=widgets.TextInput(attrs={
            'class': "form-control",
        }))
    note = CharField(
        max_length=255,
        required=False,
        widget=widgets.TextInput(attrs={
            'class': "form-control",
        }))


class MessageForm(Form):
    name = CharField(
        max_length=64,
        validators=[RegexValidator('^[A-Za-z]*[A-Za-z][A-Za-z0-9_]*$')],
        widget=widgets.TextInput(attrs={
            'class': "form-control",
        }))
    identifier = CharField(
        validators=[RegexValidator('^[a-fA-F0-9]{1,7}$')],
        widget=widgets.TextInput(attrs={
            'class': "form-control",
            'data-bs-toggle': "tooltip",
            'data-bs-placement': "bottom",
            'title': "Hex hodnota, bez 0x.",
        }))
    transmitter = CharField(
        required=False,
        max_length=255,
        widget=widgets.TextInput(attrs={
            'class': "form-control",
        }))
    receivers = CharField(
        required=False,
        max_length=255,
        widget=widgets.TextInput(attrs={
            'class': "form-control",
        }))
    note = CharField(
        max_length=255,
        required=False,
        widget=widgets.TextInput(attrs={
            'class': "form-control",
        }))


class SignalForm(Form):
    byte_types_choices = (
        (True, "Intel - little-endian"),
        (False, "Motorola - big-endian")
    )

    signed_choices = (
        (False, "unsigned"),
        (True, "signed")
    )

    is_multiplexer_choices = (
        (False, "No"),
        (True, "Yes")
    )

    name = CharField(
        max_length=64,
        validators=[RegexValidator('^[A-Za-z]*[A-Za-z][A-Za-z0-9_]*$')],
        widget=widgets.TextInput(attrs={
            'class': "form-control",
        }))
    start_bit = IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(64)],
        widget=widgets.NumberInput(attrs={
            'class': "form-control",
        }))
    length = IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(64)],
        widget=widgets.NumberInput(attrs={
            'class': "form-control",
        }))

    is_little_endian = ChoiceField(
        required=False,
        choices=byte_types_choices,
        widget=widgets.Select(attrs={
            'class': "form-select",
        }))

    is_signed = ChoiceField(
        required=False,
        choices=signed_choices,
        widget=widgets.Select(attrs={
            'class': "form-select",
        }))

    factor = IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(64)],
        widget=widgets.NumberInput(attrs={
            'class': "form-control",
        }))
    offset = IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(64)],
        widget=widgets.NumberInput(attrs={
            'class': "form-control",
        }))
    min = IntegerField(
        required=False,
        validators=[MinValueValidator(0), MaxValueValidator(64)],
        widget=widgets.NumberInput(attrs={
            'class': "form-control",
        }))
    max = IntegerField(
        required=False,
        validators=[MinValueValidator(0), MaxValueValidator(64)],
        widget=widgets.NumberInput(attrs={
            'class': "form-control",
        }))
    unit = CharField(
        required=False,
        widget=widgets.TextInput(attrs={
            'class': "form-control",
        }))
    receivers = CharField(
        required=False,
        max_length=255,
        widget=widgets.TextInput(attrs={
            'class': "form-control",
        }))
    is_multiplexer = ChoiceField(
        required=False,
        choices=is_multiplexer_choices,
        widget=widgets.Select(attrs={
            'class': "form-select",
        }))

    multiplexer_signal = ModelChoiceField(
        required=False,
        queryset=Signal.objects.filter(message=None),
        widget=widgets.Select(attrs={
            'class': "form-select",
        }))

    multiplexer_value = IntegerField(
        required=False,
        validators=[MinValueValidator(1), MaxValueValidator(64)],
        widget=widgets.NumberInput(attrs={
            'class': "form-control",
        }))
    note = CharField(
        max_length=255,
        required=False,
        widget=widgets.TextInput(attrs={
            'class': "form-control",
        }))

    def __init__(self, *args, **kwargs):
        self.message_id = kwargs.pop('message_id')
        super(SignalForm, self).__init__(*args, **kwargs)
        self.fields['multiplexer_signal'].queryset = Signal.objects.filter(
            message=self.message_id,
            is_multiplexer=True
        )


class UploadDBCForm(Form):
    name = CharField(
        max_length=255,
        widget=widgets.TextInput(attrs={
            'class': "form-control",
        }))
    file = FileField(
        widget=widgets.FileInput(attrs={
            'class': "form-control",
            'accept': ".dbc"
        }))
    note = CharField(
        max_length=255,
        required=False,
        widget=widgets.TextInput(attrs={
            'class': "form-control",
        }))

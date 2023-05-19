from django.db import models
from django.contrib.auth.models import User


class Car(models.Model):
    name = models.CharField(max_length=64)
    year = models.PositiveSmallIntegerField(blank=True, null=True)
    note = models.CharField(max_length=255, blank=True, null=True)
    author = models.CharField(max_length=150, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    changed_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        db_table = 'car'

    def __str__(self):
        return self.name


class CanBus(models.Model):
    car = models.ForeignKey('Car', on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    note = models.CharField(max_length=255, blank=True, null=True)
    author = models.CharField(max_length=150, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    changed_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        db_table = 'can_bus'
        verbose_name_plural = 'Can Buses'

    def __str__(self):
        return self.name


class Message(models.Model):
    can_bus = models.ForeignKey(CanBus, on_delete=models.CASCADE)
    identifier = models.PositiveIntegerField()
    name = models.CharField(max_length=64)
    transmitter = models.TextField(blank=True, null=True)
    receivers = models.TextField(blank=True, null=True)
    note = models.CharField(max_length=255, blank=True, null=True)
    author = models.CharField(max_length=150, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    changed_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        db_table = 'message'

    def __str__(self):
        return self.name


class Signal(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    start_bit = models.PositiveSmallIntegerField(default=0)
    length = models.PositiveSmallIntegerField(blank=True, null=True)
    is_little_endian = models.BooleanField(blank=True, null=True)
    is_signed = models.BooleanField(blank=True, null=True)
    factor = models.FloatField(default=1)
    offset = models.FloatField(default=0)
    min = models.FloatField(blank=True, null=True)
    max = models.FloatField(blank=True, null=True)
    unit = models.CharField(max_length=16, blank=True, null=True)
    receivers = models.TextField(blank=True, null=True)
    is_multiplexer = models.BooleanField(blank=True, null=True)
    multiplexer_signal = models.ForeignKey('self', on_delete=models.DO_NOTHING, blank=True, null=True)
    multiplexer_value = models.IntegerField(blank=True, null=True)
    note = models.CharField(max_length=255, blank=True, null=True)
    author = models.CharField(max_length=150, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    changed_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        db_table = 'signal'

    def __str__(self):
        return self.name


class UserPreferences(models.Model):
    user = models.CharField(primary_key=True, max_length=150) # One to one 'auth.User'
    car_name = models.BooleanField(default=0)
    car_year = models.BooleanField(default=0)
    car_note = models.BooleanField(default=0)
    car_author = models.BooleanField(default=0)
    car_created_at = models.BooleanField(default=0)
    car_changed_at = models.BooleanField(default=0)
    can_bus_name = models.BooleanField(default=0)
    can_bus_note = models.BooleanField(default=0)
    can_bus_author = models.BooleanField(default=0)
    can_bus_created_at = models.BooleanField(default=0)
    can_bus_changed_at = models.BooleanField(default=0)
    message_id = models.BooleanField(default=0)
    message_name = models.BooleanField(default=0)
    message_length = models.BooleanField(default=0)
    message_transmitter = models.BooleanField(default=0)
    message_receivers = models.BooleanField(default=0)
    message_note = models.BooleanField(default=0)
    message_author = models.BooleanField(default=0)
    message_changed_at = models.BooleanField(default=1)
    message_created_at = models.BooleanField(default=1)
    signal_name = models.BooleanField(default=0)
    signal_start_bit = models.BooleanField(default=0)
    signal_length = models.BooleanField(default=0)
    signal_is_little_endian = models.BooleanField(default=0)
    signal_is_signed = models.BooleanField(default=0)
    signal_factor = models.BooleanField(default=0)
    signal_offset = models.BooleanField(default=0)
    signal_min = models.BooleanField(default=1)
    signal_max = models.BooleanField(default=1)
    signal_unit = models.BooleanField(default=0)
    signal_receivers = models.BooleanField(default=1)
    signal_is_multiplexer = models.BooleanField(default=1)
    signal_multiplexer_signal = models.BooleanField(default=1)
    signal_multiplexer_value = models.BooleanField(default=1)
    signal_note = models.BooleanField(default=0)
    signal_author = models.BooleanField(default=1)
    signal_changed_at = models.BooleanField(default=1)
    signal_created_at = models.BooleanField(default=1)

    class Meta:
        db_table = 'user_preferences'

    def __str__(self):
        return self.user


class UserSignalCheckboxes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    signal = models.ForeignKey(Signal, on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_signal_checkboxes'


class UserMessageCheckboxes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_message_checkboxes'

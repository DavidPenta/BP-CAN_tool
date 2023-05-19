from django.contrib import admin
from .models import Car, CanBus, Message, Signal, UserPreferences, UserSignalCheckboxes, UserMessageCheckboxes


@admin.register(Car, CanBus, Message, Signal, UserPreferences, UserSignalCheckboxes, UserMessageCheckboxes)
class Admin(admin.ModelAdmin):
    pass

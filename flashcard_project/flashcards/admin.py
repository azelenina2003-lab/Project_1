from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Deck, Card

@admin.register(Deck)
class DeckAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('term', 'deck', 'created_at')
    list_filter = ('deck',)
    search_fields = ('term', 'definition')
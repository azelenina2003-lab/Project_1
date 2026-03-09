from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Deck, Card
from .forms import DeckForm, CardForm

#список колод - главная страница
def deck_list(request):
    decks = Deck.objects.all().order_by('-created_at')  # сортировка: новые сверху
    return render(request, 'flashcards/deck_list.html', {'decks': decks})

#Просмотр колоды
def deck_detail(request, pk):
    deck = get_object_or_404(Deck, pk=pk)
    cards = deck.cards.all()  
    return render(request, 'flashcards/deck_detail.html', {'deck': deck, 'cards': cards})

# Создание новой колоды
def deck_create(request):
    if request.method == 'POST':
        form = DeckForm(request.POST)
        if form.is_valid():
            deck = form.save()
            return redirect('deck_detail', pk=deck.pk)
    else:
        form = DeckForm()
    return render(request, 'flashcards/deck_form.html', {'form': form, 'title': 'Новая колода'})

# Редактирование колоды
def deck_update(request, pk):
    deck = get_object_or_404(Deck, pk=pk)
    if request.method == 'POST':
        form = DeckForm(request.POST, instance=deck)
        if form.is_valid():
            deck = form.save()
            return redirect('deck_detail', pk=deck.pk)
    else:
        form = DeckForm(instance=deck)
    return render(request, 'flashcards/deck_form.html', {'form': form, 'title': 'Редактировать колоду'})

# Удвление колоды
def deck_delete(request, pk):
    deck = get_object_or_404(Deck, pk=pk)
    if request.method == 'POST':
        deck.delete()
        return redirect('deck_list')
    return render(request, 'flashcards/deck_confirm_delete.html', {'deck': deck})

# Создание новой карточки в колоде
def card_create(request, deck_id):
    deck = get_object_or_404(Deck, pk=deck_id)
    if request.method == 'POST':
        form = CardForm(request.POST)
        if form.is_valid():
            card = form.save(commit=False)
            card.deck = deck
            card.save()
            return redirect('deck_detail', pk=deck.id)
    else:
        form = CardForm()
    return render(request, 'flashcards/card_form.html', {'form': form, 'deck': deck})

# Редактирование карточки

def card_update(request, pk):
    card = get_object_or_404(Card, pk=pk)
    if request.method == 'POST':
        form = CardForm(request.POST, instance=card)
        if form.is_valid():
            card = form.save()
            return redirect('deck_detail', pk=card.deck.id)
    else:
        form = CardForm(instance=card)
    return render(request, 'flashcards/card_form.html', {'form': form, 'deck': card.deck})

# Удаление карточки

def card_delete(request, pk):
    card = get_object_or_404(Card, pk=pk)
    deck_id = card.deck.id
    if request.method == 'POST':
        card.delete()
        return redirect('deck_detail', pk=deck_id)
    return render(request, 'flashcards/card_confirm_delete.html', {'card': card})
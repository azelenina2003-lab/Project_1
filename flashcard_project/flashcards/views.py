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
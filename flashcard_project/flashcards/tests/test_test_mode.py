import pytest
from django.urls import reverse
from .factories import CategoryFactory, EntryFactory, UserFactory

@pytest.mark.django_db
def test_test_mode_view_requires_login(client):
    """Неавторизованный пользователь перенаправляется на указание логина."""
    category = CategoryFactory()
    url = reverse('test_mode', args=[category.pk])
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))

@pytest.mark.django_db
def test_test_mode_view_shows_term(client):
    """Авторизованный пользователь видит страницу тестирования с первым термином."""
    user = UserFactory()
    client.force_login(user)
    category = CategoryFactory(user=user)
    entry = EntryFactory(category=category, term='Apple', definition='Яблоко')
    url = reverse('test_mode', args=[category.pk])
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['current_entry'] == entry
    assert b'Apple' in response.content
    assert b'Яблоко' not in response.content  # определение не показывается изначально

@pytest.mark.django_db
def test_test_mode_post_correct_answer(client):
    """Отправка правильного ответа увеличивает correct_count."""
    user = UserFactory()
    client.force_login(user)
    category = CategoryFactory(user=user)
    entry = EntryFactory(category=category, term='Apple', definition='Яблоко', correct_count=0, wrong_count=0)
    url = reverse('test_mode', args=[category.pk])
    data = {'answer': 'Яблоко'}
    response = client.post(url, data)
    assert response.status_code == 200
    # Обновляем объект 
    entry.refresh_from_db()
    assert entry.correct_count == 1
    assert entry.wrong_count == 0
    # Проверка, что в контексте result=True
    assert response.context['result'] is True

@pytest.mark.django_db
def test_test_mode_post_wrong_answer(client):
    """Отправка неправильного ответа увеличивает wrong_count и показывает правильный ответ."""
    user = UserFactory()
    client.force_login(user)
    category = CategoryFactory(user=user)
    entry = EntryFactory(category=category, term='Apple', definition='Яблоко', correct_count=0, wrong_count=0)
    url = reverse('test_mode', args=[category.pk])
    data = {'answer': 'Груша'}
    response = client.post(url, data)
    assert response.status_code == 200
    entry.refresh_from_db()
    assert entry.correct_count == 0
    assert entry.wrong_count == 1
    assert response.context['result'] is False
    # Проверка, что правильный ответ отображается
    assert b'Яблоко' in response.content

@pytest.mark.django_db
def test_test_mode_navigation(client):
    """Проверка переключения между терминами через параметр index."""
    user = UserFactory()
    client.force_login(user)
    category = CategoryFactory(user=user)
    entry1 = EntryFactory(category=category, term='Apple')
    entry2 = EntryFactory(category=category, term='Banana')
    url = reverse('test_mode', args=[category.pk])
    # Переход ко второму термину
    response = client.get(url, {'index': 1})
    assert response.status_code == 200
    assert response.context['current_index'] == 1
    assert response.context['current_entry'] == entry2

@pytest.mark.django_db
def test_test_mode_no_entries(client):
    """Если в категории нет записей, отображается сообщение."""
    user = UserFactory()
    client.force_login(user)
    category = CategoryFactory(user=user)
    url = reverse('test_mode', args=[category.pk])
    response = client.get(url)
    assert response.status_code == 200
    assert b'нет записей' in response.content.lower()

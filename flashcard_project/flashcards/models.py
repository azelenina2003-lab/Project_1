from django.db import models

# Create your models here.
from django.db import models
from django.urls import reverse

class Category (models.Model):
    """Колода карточек"""
    name = models.CharField('Название', max_length=200)
    description = models.TextField('Описание', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Колода'
        verbose_name_plural = 'Колоды'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('deck_detail', args=[str(self.id)])


class Entry(models.Model):
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='entries',      # чтобы можно было писать category.entries.all()
        verbose_name='Категория'
    )
    term = models.CharField('Термин', max_length=200)
    definition = models.TextField('Определение')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    def __str__(self):
        return self.term  # или f'{self.term} - {self.category.name}'

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
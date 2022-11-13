import uuid

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date
from tinymce.models import HTMLField

# Create your models here.
class Genre(models.Model):
    name = models.CharField('Projektas', max_length=100, help_text='Nurodykite projekto etapą (pvz. techninis projektas)')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Projekto etapas'
        verbose_name_plural = 'Projekto etapai'


class Book(models.Model):
    """Modelis reprezentuojantis knygą"""
    title = models.CharField('Projekto kodas', max_length=200)
    author = models.ForeignKey('Author', max_length=200, null=True, on_delete=models.SET_NULL, related_name='books')
    summary = models.TextField('Aprašymas', max_length=1000, help_text='Trumpas projekto aprašymas')
    isbn = models.CharField('ISBN', max_length=13, help_text='13 simbolių unikalus ISBN kodas')
    genre = models.ManyToManyField(Genre, help_text='Išsirinkite projekto etapą')
    cover = models.ImageField('Viršelis', upload_to='covers', null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Nurodo konkretaus knygos aprašymo galutinį adresą"""
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        return ','.join(genre.name for genre in self.genre.all()[:3])

class BookInstance(models.Model):
    """Modelis aprašantis konkrečios knygos kopijos būseną"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unikalus ID projekto kopijai')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    due_back = models.DateField('Bus prieinama', null=True, blank=True)
    reader = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    LOAN_STATUS = (
        ('a', 'Projektas nepradėtas'),
        ('p', 'Projekto laikas eina į pabaigą'),
        ('g', 'Projektas baigtas'),
        ('r', 'Dirbama')
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, default='a', help_text='Statusas', blank=True)

    class Meta:
        ordering = ['due_back']

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    def __str__(self):
        return f'{self.id} {self.book.title}'

class Author(models.Model):
    """Modelis reprezentuojantis knygos autorių."""
    first_name = models.CharField('Vardas', max_length=80)
    last_name = models.CharField('Pavardė', max_length=80)
    description = HTMLField()
    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Nurodo konkretaus autoriaus galutinį adresą"""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

    def display_books(self):
        return ', '.join(book.title for book in self.books.all()[:3])

    display_books.short_description = 'Projektai'

class BookReview(models.Model):
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True, blank=True)
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField('Atsiliepimai', max_length=200)
    date_created = models.DateField(auto_now_add=True)

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg
from .models import Reviews, Books  # Импортируем модели

@receiver(post_save, sender=Reviews)
@receiver(post_delete, sender=Reviews)
def update_book_rating(sender, instance, **kwargs):
    """
    Обновляет рейтинг книги при сохранении или удалении отзыва.
    """
    book = instance.book
    # Вычисляем средний рейтинг
    result = book.reviews_set.aggregate(average_rating=Avg('rating'))
    book.rating = result['average_rating'] if result['average_rating'] is not None else 0
    book.save()
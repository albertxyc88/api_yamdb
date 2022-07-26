from django.db import models


class Review(models.Model):
    text = models.TextField(blank=False, verbose_name='Текст',)
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата отзыва',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='review'
        verbose_name='Автор',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='review',
        verbose_name='Произведения',
    )
    score = models.IntegerField(verbose_name='Рейтинг')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('title')

    def __str__(self):
        return self.title


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='comments',
        verbose_name='Автор',
    )
    text = models.TextField(blank=False, verbose_name='Текст',)
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата комментария',
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('review')

    def __str__(self):
        return self.review[:15]
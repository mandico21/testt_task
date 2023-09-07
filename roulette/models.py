import uuid

from django.db import models


class TimedBaseModel(models.Model):
    """Основная модель с датой"""

    class Meta:
        abstract = True

    created_at = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name='Дата последнего обновления',
        auto_now=True
    )


class Cell(TimedBaseModel):
    class Meta:
        verbose_name = 'Ячейка'
        verbose_name_plural = 'Ячейки'

    number = models.PositiveIntegerField(
        verbose_name='Ячейка',
        unique=True
    )
    weight = models.IntegerField(
        verbose_name='Вес',
        null=True,
        blank=True,
    )
    is_jackpot = models.BooleanField(
        verbose_name='Джекпот',
        default=False,
    )

    def __str__(self) -> str:
        return f'{self.number}'


class Round(TimedBaseModel):
    class Meta:
        verbose_name = 'Раунд'
        verbose_name_plural = 'Раунды'

    round_number = models.AutoField(
        verbose_name='Номер раунда',
        primary_key=True,
    )
    cells = models.ManyToManyField(
        Cell,
        verbose_name='Ячейки',
        blank=True,
    )
    is_jackpot_drawn = models.BooleanField(
        verbose_name='Джекпот выпал',
        default=False,
    )

    def __str__(self) -> str:
        return f'{self.round_number} / {self.is_jackpot_drawn}'


class Player(TimedBaseModel):
    class Meta:
        verbose_name = 'Игрок'
        verbose_name_plural = 'Игроки'

    id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        primary_key=True,
    )
    name = models.CharField(
        verbose_name='Имя',
        max_length=100
    )

    def __str__(self) -> str:
        return self.name


class Participant(models.Model):
    class Meta:
        verbose_name = 'Раунд рулеток'
        verbose_name_plural = 'Раунды рулеток'
        unique_together = ('round', 'cell_number',)

    round = models.ForeignKey(
        Round,
        verbose_name='Раунд',
        related_name='roulette_rounds',
        on_delete=models.CASCADE,
    )
    cell_number = models.ForeignKey(
        Cell,
        verbose_name='Ячейка',
        on_delete=models.CASCADE,
    )
    player = models.ForeignKey(
        Player,
        verbose_name='Участник',
        related_name='roulette_rounds',
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return f'{self.player} / Раунд: {self.round} - {self.cell_number}'

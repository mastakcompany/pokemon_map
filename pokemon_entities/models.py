from django.db import models


class Pokemon(models.Model):
    title = models.CharField(max_length=200, verbose_name='Имя покемона')
    title_en = models.CharField(
        max_length=200,
        verbose_name='Имя покемона (En)',
        null=True,
        blank=True
    )
    title_jp = models.CharField(
        max_length=200,
        verbose_name='Имя покемона (Jp)',
        null=True,
        blank=True
    )
    photo = models.ImageField(verbose_name='Фото')
    description = models.TextField(
        verbose_name='Описание',
        null=True,
        blank=True
    )
    previous_evolution = models.ForeignKey(
        "self", on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="pokemon_entities",
        verbose_name='Из кого эволюционировал'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Покемон'
        verbose_name_plural = 'Покемоны'


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        verbose_name='Имя покемона'
    )
    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')
    appeared_at = models.DateTimeField(
        verbose_name='Начало отображения на карте'
    )
    disappeared_at = models.DateTimeField(
        verbose_name='Конец отображения на карте'
    )
    level = models.IntegerField(
        verbose_name='Уровень',
        null=True,
        blank=True
    )
    health = models.IntegerField(
        verbose_name='Здоровье',
        null=True,
        blank=True
    )
    strength = models.IntegerField(
        verbose_name='Атака',
        null=True,
        blank=True
    )
    defence = models.IntegerField(
        verbose_name='Защита',
        null=True,
        blank=True
    )
    stamina = models.IntegerField(
        verbose_name='Выносливость',
        null=True,
        blank=True
    )

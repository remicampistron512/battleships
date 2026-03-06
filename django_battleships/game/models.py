from django.core.exceptions import ValidationError
from django.db import models
from django.db.utils import OperationalError, ProgrammingError


def validate_hex_color(value):
    if len(value) != 7 or not value.startswith('#'):
        raise ValidationError('Use a hex color value such as #0ea5e9.')
    valid_chars = '0123456789abcdefABCDEF'
    if any(char not in valid_chars for char in value[1:]):
        raise ValidationError('Use a valid hex color value.')


class GameSettings(models.Model):
    grid_size = models.PositiveSmallIntegerField(default=10)
    water_color = models.CharField(max_length=7, default='#0369a1', validators=[validate_hex_color])
    grid_line_color = models.CharField(max_length=7, default='#7dd3fc', validators=[validate_hex_color])
    hit_color = models.CharField(max_length=7, default='#ef4444', validators=[validate_hex_color])
    miss_color = models.CharField(max_length=7, default='#f8fafc', validators=[validate_hex_color])
    ship_color = models.CharField(max_length=7, default='#22c55e', validators=[validate_hex_color])

    class Meta:
        verbose_name_plural = 'Game settings'

    def clean(self):
        if not 6 <= self.grid_size <= 20:
            raise ValidationError({'grid_size': 'Grid size must be between 6 and 20.'})

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        try:
            instance = cls.objects.first()
        except (OperationalError, ProgrammingError):
            return cls()
        if instance:
            return instance
        return cls()

    def __str__(self):
        return 'Battleships settings'

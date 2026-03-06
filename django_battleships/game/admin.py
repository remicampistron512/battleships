from django.contrib import admin

from .models import GameSettings


@admin.register(GameSettings)
class GameSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            'Board settings',
            {
                'fields': ('grid_size',),
            },
        ),
        (
            'Color settings',
            {
                'fields': ('water_color', 'grid_line_color', 'hit_color', 'miss_color', 'ship_color'),
            },
        ),
    )

    def has_add_permission(self, request):
        return not GameSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

from django.contrib import admin

from roulette.models import Round, Cell, Player, Participant


@admin.register(Round)
class RoundAdmin(admin.ModelAdmin):
    list_display = ('round_number', 'is_jackpot_drawn')


@admin.register(Cell)
class CellAdmin(admin.ModelAdmin):
    list_display = ('number', 'weight', 'is_jackpot')


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    readonly_fields = ('id',)


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('round', 'player', 'cell_number')

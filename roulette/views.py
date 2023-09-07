from random import choices

from django.db import transaction
from django.db.models import Count, Avg
from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView

from roulette.models import Round, Cell, Participant, Player


class SpinRouletteAPI(APIView):

    @transaction.atomic
    def post(self, request):
        """
         player_id: UUID = ID игрока
        """
        player_id = request.data.get('player_id')
        round_obj, created = Round.objects.get_or_create(
            is_jackpot_drawn=False)
        if created:
            cells = Cell.objects.all()
            round_obj.cells.set(cells)
            
        cells = round_obj.cells.filter(is_jackpot=False).all()

        if cells.exists():
            cell = choices(cells,
                           weights=[cell.weight for cell in cells])[0]
            message = f'Вам выпала ячейка {cell}'
        else:
            round_obj.is_jackpot_drawn = True
            round_obj.save()
            cell = round_obj.cells.filter(is_jackpot=True).first()
            message = 'Поздравляем! Вы выиграли джекпот'

        Participant.objects.create(
            round=round_obj,
            cell_number=cell,
            player_id=player_id
        )
        round_obj.cells.remove(cell)
        return JsonResponse(
            data={'player_id': player_id, 'message': message},
            status=status.HTTP_200_OK
        )


class StaticSpinAPI(APIView):

    def get(self, request):
        # Сделал вывод уникальных пользователей,
        # distinct=True - убрать данный аргумент и будет выводить общее кол-во
        rounds = Round.objects.annotate(
            count_players=Count(
                expression='roulette_rounds__player', distinct=True
            )
        ).values('round_number', 'count_players', 'is_jackpot_drawn')

        response = list(rounds)

        return JsonResponse(
            data=response,
            status=status.HTTP_200_OK,
            safe=False,
        )


class StaticUserAPI(APIView):

    def get(self, request):
        players_data = Player.objects.annotate(
            count_rounds=Count(
                expression='roulette_rounds__round_id',
                distinct=True),
            average_rounds=Avg('roulette_rounds__cell_number')
        ).values('id', 'count_rounds', 'average_rounds')

        response = list(players_data)

        return JsonResponse(
            data=response,
            status=status.HTTP_200_OK,
            safe=False
        )

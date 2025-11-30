import datetime
from django.db.models import F, PositiveSmallIntegerField, ExpressionWrapper
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.db.models.functions import ExtractYear, Abs, Coalesce
from .models import *
from django.db.models import Sum, Q, F, FloatField
from django.shortcuts import render


class HomeView(View):
    def get(self, request):
        return render(request, 'index.html')

class ClubsView(View):
    def get(self, request):
        clubs = Club.objects.all()
        country = request.GET.get('country')
        if country:
            clubs = clubs.filter(country__name=country)


        context = {
            'clubs': clubs
        }
        return render(request, 'clubs.html', context)

class ClubDetailsView(View):
    def get(self, request, pk):
        club = get_object_or_404(Club, id=pk)
        players = club.player_set.all()
        context = {
            'club': club,
            'players': players
        }
        return render(request, 'club-details.html', context)

class AboutView(View):
    def get(self, request):
        return render(request, 'about.html')

class TryoutView(View):
    def get(self, request):
        return render(request, 'tryouts.html')

class LatestTransfersView(View):
    def get(self, request):
        players = Player.objects.all()
        transfers = Transfer.objects.filter(season=Season.objects.last()).order_by('-price')
        context = {
            'players': players,
            'transfers': transfers
        }
        return render(request, 'latest-transfers.html', context)

class PlayersView(View):
    def get(self, request):
        players = Player.objects.all()
        context = {
            'players': players
        }
        return render(request, 'players.html', context)

class U_20_playersView(View):
    def get(self, request):
        now_year = int(datetime.datetime.now().year)
        players = Player.objects.annotate(
            age=ExpressionWrapper(
                now_year - ExtractYear('birth_date'),
                output_field=PositiveSmallIntegerField()
            )
        ).filter(age__lte=20).order_by('-price')
        context = {
            'players': players,
        }
        return render(request, 'players.html', context)

class StatsView(View):
    def get(self, request):
        context = {
            'last_season': Season.objects.last(),
        }
        return render(request, 'stats.html', context)

class CountryView(View):
    def get(self, request):
        countries = Country.objects.all()
        clubs = Club.objects.all()
        context = {
            'countries': countries,
            'clubs': clubs
        }
        return render(request, 'country.html', context)

class Top150AccuratePredictions(View):
    def get(self, request):
        top_accurate_transfers = Transfer.objects.annotate(
            moa = Abs(
                (1 - F('price') / F('price_tft')) * 100
            )
        ).order_by('moa')[:150]
        context = {
            'top_accurate_transfers': top_accurate_transfers,
        }
        return render(request, 'stats/top-150-accurate-predictions.html', context)

class TransferRecords(View):
    def get(self, request):
        transfers = Transfer.objects.filter(price__gte=50).order_by('-price')
        context = {
            'transfers': transfers
        }
        return render(request, 'stats/transfer-records.html', context)

class Top50ClubsByExpenditure(View):
    def get(self, request):
        clubs = Club.objects.annotate(
            total_expense=Sum("import_transfers__price")
        ).order_by('-total_expense')[:50]
        context = {
            'last_season': Season.objects.last(),
            'clubs': clubs
        }
        return render(request, 'stats/top-50-clubs-by-expenditure.html', context)

class Top50ClubsByIncome(View):
    def get(self, request):
        last_season = Season.objects.last()  # Define it first

        clubs = Club.objects.annotate(
            total_income=Coalesce(
                Sum(
                    'export_transfers__price',
                    filter=Q(export_transfers__season=last_season)
                ),
                0,
                output_field=FloatField()  # <- add this
            )
        ).order_by('-total_income')[:50]

        context = {
            'last_season': last_season,
            'clubs': clubs
        }
        return render(request, 'stats/top-50-clubs-by-income.html', context)
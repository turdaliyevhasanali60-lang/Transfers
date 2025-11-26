from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from main.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',  HomeView.as_view(), name='home'),
    path('clubs/', ClubsView.as_view(), name='clubs'),
    path('clubs/<int:pk>/details', ClubDetailsView.as_view(), name='club-details'),
    path('about/', AboutView.as_view(), name='about'),
    path('tryouts/', TryoutView.as_view(), name='tryouts'),
    path('latest-transfers/', LatestTransfersView.as_view(), name='latest-transfers'),
    path('players/', PlayersView.as_view(), name='players'),
    path('20-players/', U_20_playersView.as_view(), name='20-players'),
    path('stats/', StatsView.as_view(), name='stats'),
    path('country/<int:pk>/details', CountryView.as_view(), name='country'),
    path('top-150-accurate-predictions/', Top150AccuratePredictions.as_view(), name='top-150-accurate-predictions'),
    path('transfer-records/', TransferRecords.as_view(), name='transfer-records'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
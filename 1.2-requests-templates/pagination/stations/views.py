from django.shortcuts import render, redirect
from django.urls import reverse
import csv
from django.core.paginator import Paginator
from pagination.settings import BUS_STATION_CSV


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    with open(BUS_STATION_CSV, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        reader_list = [read for read in reader]
        page_number = int(request.GET.get("page", 1))
        paginator = Paginator(reader_list, 10)
        page = paginator.get_page(page_number)
        bus_stations = [stations for stations in page]
        # получите текущую страницу и передайте ее в контекст
        # также передайте в контекст список станций на странице

        context = {
            'bus_stations': bus_stations,
            'page': page,
        }
        return render(request, 'stations/index.html', context=context)

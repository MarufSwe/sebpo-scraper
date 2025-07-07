from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..models import ScrapedItem
from ..utils import scrape_fincen
from django.contrib.auth.decorators import login_required


@login_required
def item_list(request):
    items = ScrapedItem.objects.all().order_by('name')
    return render(request, 'scraper/item_list.html', {'items': items})


@login_required
def refresh_data(request):
    if request.method == "POST":
        changes = scrape_fincen()
        return JsonResponse(changes)
    return JsonResponse({"error": "Only POST allowed"}, status=400)
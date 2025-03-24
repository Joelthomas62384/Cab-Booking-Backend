import requests
from django.http import JsonResponse
from django.conf import settings

def get_places(request):
    input_text = request.GET.get("input")
    
    if not input_text:
        return JsonResponse({"error": "Missing input query"}, status=400)

    api_key = settings.GOOGLE_MAPS_API_KEY
    api_url = f"https://maps.googleapis.com/maps/api/place/autocomplete/json?input={input_text}&key={api_key}&types=geocode"

    try:
        response = requests.get(api_url)
        data = response.json()
        print(data)
        return JsonResponse(data)
    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": "Failed to fetch places", "details": str(e)}, status=500)

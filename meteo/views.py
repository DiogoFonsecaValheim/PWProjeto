# meteo/views.py
from django.shortcuts import render
import requests
from django.http import JsonResponse

URL_TIPOS_CLIMA_IPMA = 'https://api.ipma.pt/open-data/weather-type-classe.json'

def obter_tipos_clima():
    resposta = requests.get(URL_TIPOS_CLIMA_IPMA)
    return resposta.json() if resposta.status_code == 200 else None

def today_weather(request):
    city_id = 1110600  # ID de Lisboa na API do IPMA
    weather_url = f'https://api.ipma.pt/open-data/forecast/meteorology/cities/daily/{city_id}.json'
    weather_types_response = obter_tipos_clima()

    weather_response = requests.get(weather_url).json()

    if not weather_types_response:
        return JsonResponse({'error': 'Não foi possível obter os tipos de clima'}, status=500)

    weather_types = {wt['idWeatherType']: wt['descWeatherTypePT'] for wt in weather_types_response['data']}

    today_forecast = weather_response['data'][0]
    weather_type_id = today_forecast['idWeatherType']

    weather_description = weather_types.get(weather_type_id, 'Descrição indisponível')

    if weather_type_id < 10:
        icone_clima = f"/static/meteo/w_ic_d_0{weather_type_id}anim.svg"
    else:
        icone_clima = f"/static/meteo/w_ic_d_{weather_type_id}anim.svg"

    context = {
        'city_name': 'Lisboa',
        'temp_min': today_forecast['tMin'],
        'temp_max': today_forecast['tMax'],
        'date': today_forecast['forecastDate'],
        'weather_description': weather_description,
        'icon': icone_clima
    }

    return render(request, 'meteo/today_weather.html', context)


# Endpoint para a previsão dos próximos 5 dias
def five_days_weather(request):
    city_id = request.GET.get('city_id', 1110600)  # Default: Lisboa
    weather_url = f'https://api.ipma.pt/open-data/forecast/meteorology/cities/daily/{city_id}.json'
    cities_url = 'https://api.ipma.pt/open-data/distrits-islands.json'

    weather_response = requests.get(weather_url).json()
    cities_response = requests.get(cities_url).json()
    weather_types_response = obter_tipos_clima()

    if not weather_types_response:
        return JsonResponse({'error': 'Não foi possível obter os tipos de clima'}, status=500)

    weather_types = {wt['idWeatherType']: wt['descWeatherTypePT'] for wt in weather_types_response['data']}

    forecasts = weather_response['data'][:5]
    for forecast in forecasts:
        weather_type_id = forecast['idWeatherType']
        forecast['weather_description'] = weather_types.get(weather_type_id, 'Descrição indisponível')

        if weather_type_id < 10:
            forecast['icon'] = f"/static/meteo/w_ic_d_0{weather_type_id}anim.svg"
        else:
            forecast['icon'] = f"/static/meteo/w_ic_d_{weather_type_id}anim.svg"

    context = {
        'city_name': next((city['local'] for city in cities_response['data'] if city['globalIdLocal'] == int(city_id)), 'Lisboa'),
        'forecasts': forecasts,
        'cities': cities_response['data']
    }

    return render(request, 'meteo/five_days_weather.html', context)


def lista_cidades(request):
    cities_url = 'https://api.ipma.pt/open-data/distrits-islands.json'
    response = requests.get(cities_url)
    cities_data = response.json()

    cities_dict = {city['globalIdLocal']: city['local'] for city in cities_data['data']}
    return JsonResponse(cities_dict)

def previsao_hoje(request, cidade_id):
    city_weather_url = f'https://api.ipma.pt/open-data/forecast/meteorology/cities/daily/{cidade_id}.json'
    response = requests.get(city_weather_url)
    weather_data = response.json()

    today_forecast = weather_data['data'][0]
    weather_description = today_forecast['descIdWeatherTypePT']

    today_forecast_dict = {
        'nome_da_cidade': today_forecast['local'],
        'temperatura_minima': today_forecast['tMin'],
        'temperatura_maxima': today_forecast['tMax'],
        'data': today_forecast['forecastDate'],
        'descricao_tempo': weather_description,
        'precipitacao': today_forecast['precipitaProb'],
        'icone_tempo': f"/static/meteo/w_ic_d_{today_forecast['idWeatherType']}anim.svg"
    }
    return JsonResponse(today_forecast_dict)

def previsao_5_dias(request, cidade_id):
    city_weather_url = f'https://api.ipma.pt/open-data/forecast/meteorology/cities/daily/{cidade_id}.json'
    response = requests.get(city_weather_url)
    weather_data = response.json()

    forecasts = weather_data['data'][:5]
    forecasts_list = []
    for forecast in forecasts:
        weather_description = forecast['descIdWeatherTypePT']
        forecast_dict = {
            'nome_da_cidade': forecast['local'],
            'temperatura_minima': forecast['tMin'],
            'temperatura_maxima': forecast['tMax'],
            'data': forecast['forecastDate'],
            'descricao_tempo': weather_description,
            'precipitacao': forecast['precipitaProb'],
            'icone_tempo': f"/static/meteo/w_ic_d_{forecast['idWeatherType']}anim.svg"
        }
        forecasts_list.append(forecast_dict)
    return JsonResponse(forecasts_list, safe=False)

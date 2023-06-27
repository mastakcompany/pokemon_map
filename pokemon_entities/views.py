import folium

from django.shortcuts import render
from django.utils.timezone import localtime
from pokemon_entities.models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    base_url = request.build_absolute_uri('/media/')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in PokemonEntity.objects.filter(appeared_at__lte=localtime(), disappeared_at__gt=localtime()):
        add_pokemon(
            folium_map, pokemon.lat,
            pokemon.lon,
            f"{base_url}{pokemon.pokemon.photo}"
        )

    pokemons_on_page = []
    for pokemon in Pokemon.objects.all():
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': f"{base_url}{pokemon.photo}",
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    requested_pokemon = Pokemon.objects.get(id=pokemon_id)
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    pokemon_entities = PokemonEntity.objects.filter(
        appeared_at__lte=localtime(),
        disappeared_at__gt=localtime(),
        pokemon=requested_pokemon
    )

    base_url = request.build_absolute_uri('/media/')

    for pokemon in pokemon_entities:
        add_pokemon(
            folium_map,
            pokemon.lat,
            pokemon.lon,
            f"{base_url}{pokemon.pokemon.photo}"
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(),
        'pokemon': {
            'pokemon_id': requested_pokemon.id,
            'img_url': f"{base_url}{requested_pokemon.photo}",
            'title_ru': requested_pokemon.title,
            'title_en': requested_pokemon.title_en,
            'title_jp': requested_pokemon.title_jp,
            'description': requested_pokemon.description,
            'previous_evolution': {
                'pokemon_id': requested_pokemon.previous_evolution.id,
                'img_url': f"{base_url}{requested_pokemon.previous_evolution.photo}",
                'title_ru': requested_pokemon.previous_evolution.title
            } if requested_pokemon.previous_evolution else None,
            'next_evolution': {
                'pokemon_id': requested_pokemon.pokemon_entities.all()[0].id,
                'img_url': f"{base_url}{requested_pokemon.pokemon_entities.all()[0].photo}",
                'title_ru': requested_pokemon.pokemon_entities.all()[0].title
            } if requested_pokemon.pokemon_entities.all() else None
        }
    })

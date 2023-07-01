import folium

from django.shortcuts import render, get_object_or_404
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
    current_time = localtime()

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in PokemonEntity.objects.filter(appeared_at__lte=current_time, disappeared_at__gt=current_time):
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon_entity.pokemon.photo.url)
        )

    pokemons_on_page = []
    for pokemon in Pokemon.objects.all():
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(pokemon.photo.url),
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    requested_pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    current_time = localtime()

    pokemon_entities = PokemonEntity.objects.filter(
        appeared_at__lte=current_time,
        disappeared_at__gt=current_time,
        pokemon=requested_pokemon
    )

    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon_entity.pokemon.photo.url)
        )

    pokemon_serialized = {
        'pokemon_id': requested_pokemon.id,
        'img_url': request.build_absolute_uri(requested_pokemon.photo.url),
        'title_ru': requested_pokemon.title,
        'title_en': requested_pokemon.title_en,
        'title_jp': requested_pokemon.title_jp,
        'description': requested_pokemon.description,
    }

    if requested_pokemon.previous_evolution:
        previous_evolution = requested_pokemon.previous_evolution
        pokemon_serialized['previous_evolution'] = {
            'pokemon_id': previous_evolution.id,
            'img_url': request.build_absolute_uri(previous_evolution.photo.url),
            'title_ru': previous_evolution.title
        }

    if next_evolution := requested_pokemon.next_evolutions.first():
        pokemon_serialized['next_evolution'] = {
            'pokemon_id': next_evolution.id,
            'img_url': request.build_absolute_uri(next_evolution.photo.url),
            'title_ru': next_evolution.title
        }

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(),
        'pokemon': pokemon_serialized
    })

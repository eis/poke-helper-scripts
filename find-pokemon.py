import json
import sys

with open('pokemon-basedata.json', 'r') as f:
  pokemons = json.load(f)

pokemon_to_find = sys.argv[1].upper()

for pokemon in pokemons:
  if (pokemon_to_find in pokemon['pokemonId']):
    print(pokemon['pokemonId'])
    for moveset in pokemon['movesets']:
      print(moveset['quickMove'] + ' - ' + moveset['cinematicMove'])

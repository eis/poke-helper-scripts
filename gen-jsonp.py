import shutil

shutil.copy('pokemons.json', 'pokemons.jsonp')
with open('pokemons.jsonp', 'r+') as f:
    content = f.read()
    f.seek(0, 0)
    f.write('var pokemons = ' + content)
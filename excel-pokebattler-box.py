import sys
import json
import copy
import pandas

inputstr = sys.stdin.read()
respjson = json.loads(inputstr)

#with open('pokemons.json') as f:
#    respjson = json.load(f)

def format_move(string):
  return ''.join(list(map(lambda x: x[0], string.lower().split('_'))))


excel_json = []
for pokemon in respjson:
  newpoke = copy.deepcopy(pokemon)
  newpoke['iv'] = '{}/{}/{}'.format(pokemon['individualAttack'],pokemon['individualDefense'],pokemon['individualStamina'])
  del newpoke['individualAttack']
  del newpoke['individualDefense']
  del newpoke['individualStamina']
  newpoke['pokemon'] = newpoke['pokemon'].lower().replace('_alola_form','')
  newpoke['quickMove'] = newpoke['quickMove'].replace('_FAST','')
  newpoke['moveset'] = '{}/{}'.format(format_move(newpoke['quickMove']),format_move(newpoke['cinematicMove']))
  excel_json.append(newpoke)

cols = ['pokemon','level','iv','cp','moveset']
df = pandas.DataFrame(excel_json, columns=cols)
df.set_index('pokemon', inplace=True)
print(df)

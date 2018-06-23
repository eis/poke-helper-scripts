import http.client
import json
import sys
import copy

# https://www.pokebattler.com/fights/attackers/ABRA/quickMoves/ZEN_HEADBUTT_FAST/cinMoves/PSYSHOCK/levels/34/ivs/FEF/defenders/MEWTWO/quickMoves/CONFUSION_FAST/cinMoves/FOCUS_BLAST/cp/49430/strategies/DODGE_SPECIALS/DEFENSE_RANDOM_MC?includeDetails=true&dodgeStrategy=DODGE_REACTION_TIME&weatherCondition=NO_WEATHER&seed=1529739050358
# https://fight.pokebattler.com/fights/attackers/ABRA/quickMoves/ZEN_HEADBUTT_FAST/cinMoves/PSYSHOCK/levels/34/ivs/FEF/defenders/MEWTWO/quickMoves/CONFUSION_FAST/cinMoves/FOCUS_BLAST/cp/49430/strategies/DODGE_SPECIALS/DEFENSE_RANDOM_MC?includeDetails=true&dodgeStrategy=DODGE_REACTION_TIME&weatherCondition=NO_WEATHER&seed=1529739050358

# inputstr = sys.stdin.read()
inputstr = """[ {
        "pokemon": "DRAGONITE",
        "individualStamina": 12,
        "cinematicMove": "OUTRAGE",
        "quickMove": "DRAGON_TAIL_FAST",
        "cp": 3263,
        "name": "",
        "id": 1392252,
        "level": "34.5",
        "individualDefense": 15,
        "individualAttack": 14
    } ]"""
respjson = json.loads(inputstr)

def format_move(string):
  return ''.join(list(map(lambda x: x[0], string.lower().split('_'))))

def format_ivs(attack, defense, stamina):
  return '%X%X%X' %(attack, defense, stamina)

def fetch_for(pokemon, defender='MEWTWO', def_quick='CONFUSION_FAST', def_charge='FOCUS_BLAST', def_cp='49430'):
  print('fetching for %s (cp %s)' % (pokemon['pokemon'], pokemon['cp']), file=sys.stderr)

  url = '/fights/attackers/{}/quickMoves/{}/cinMoves/{}/levels/{}/ivs/{}/defenders/{}/quickMoves/{}/cinMoves/{}/cp/{}/strategies/DODGE_SPECIALS/DEFENSE_RANDOM_MC?includeDetails=false&dodgeStrategy=DODGE_REACTION_TIME&weatherCondition=NO_WEATHER&seed=1529739050358'.format(
    pokemon['pokemon'], pokemon['quickMove'], pokemon['cinematicMove'], pokemon['level'], format_ivs(pokemon['individualAttack'], pokemon['individualDefense'], pokemon['individualStamina']),
    defender, def_quick, def_charge, def_cp)
  # print('url ' + url)
  conn = http.client.HTTPSConnection('fight.pokebattler.com', 443)
  # conn.set_debuglevel(1)
  conn.putrequest('GET', url)
  conn.putheader('User-Agent', sys.argv[0])
  conn.putheader('Accept', 'application/json')
  conn.putheader('Accept-Language','en-US,en;q=0.5')
  conn.putheader('Referer','https://www.pokebattler.com/pokebox')
  conn.putheader('Origin','https://www.pokebattler.com')
  conn.putheader('Cache-Control','max-age=0')
  conn.endheaders()
  r = conn.getresponse()
  return r.read().decode("utf-8")

results = []

for pokemon in respjson:
  #print(json.dumps(pokemon, indent=4))
  #break

  # resp = fetch_for(pokemon, sys.argv[1].upper(), sys.argv[2].upper(), sys.argv[3].upper(), sys.argv[4].upper())
  resp = fetch_for(pokemon)
  fightdata = json.loads(resp)

  # with open('data-formatted.json') as f:
  # fightdata = json.load(f)

  del fightdata['fightParameters']
  del fightdata['combatants']

  # print(json.dumps(fightdata, indent=4))

  fightdata['pokemon'] = pokemon['pokemon'].lower().replace('_alola_form','')
  fightdata['cp'] = pokemon['cp']
  fightdata['level'] = pokemon['level']
  fightdata['iv'] = '{}/{}/{}'.format(pokemon['individualAttack'],pokemon['individualDefense'],pokemon['individualStamina'])
  fightdata['moveset'] = '{}/{}'.format(format_move(pokemon['quickMove'].replace('_FAST','')),format_move(pokemon['cinematicMove']))
  fightdata['effectiveCombatTime'] = round(fightdata['effectiveCombatTime'] / 1000, 1)
  fightdata['power'] = round(fightdata['power'] * 100, 1)
  fightdata['overallRating'] = round(fightdata['overallRating'] * 100, 1)

  results.append(fightdata)



#print(df.sort_values('overallRating', ascending=False))
print(json.dumps(results, indent=4))

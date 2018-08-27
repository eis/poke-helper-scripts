from __future__ import print_function

from flask import Flask
from flask import request
from time import strftime

import json
import http.client
import sys
import copy

# https://www.pokebattler.com/fights/attackers/ABRA/quickMoves/ZEN_HEADBUTT_FAST/cinMoves/PSYSHOCK/levels/34/ivs/FEF/defenders/MEWTWO/quickMoves/CONFUSION_FAST/cinMoves/FOCUS_BLAST/cp/49430/strategies/DODGE_SPECIALS/DEFENSE_RANDOM_MC?includeDetails=true&dodgeStrategy=DODGE_REACTION_TIME&weatherCondition=NO_WEATHER&seed=1529739050358
# https://fight.pokebattler.com/fights/attackers/ABRA/quickMoves/ZEN_HEADBUTT_FAST/cinMoves/PSYSHOCK/levels/34/ivs/FEF/defenders/MEWTWO/quickMoves/CONFUSION_FAST/cinMoves/FOCUS_BLAST/cp/49430/strategies/DODGE_SPECIALS/DEFENSE_RANDOM_MC?includeDetails=true&dodgeStrategy=DODGE_REACTION_TIME&weatherCondition=NO_WEATHER&seed=1529739050358

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

def do_the_pokemon(respjson):
  results = []

  for pokemon in respjson['pokemons']:
    #print(json.dumps(pokemon, indent=4))

    resp = fetch_for(pokemon, respjson['defenderId'], respjson['fastMove'], respjson['chargedMove'], respjson['defenderCp'])
    # resp = fetch_for(pokemon)
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

  return results


print('Loading function')


def handler(event, context):
    '''Provide an event that contains the following keys:
      - operation: one of the operations in the operations dict below
      - tableName: required for operations that interact with DynamoDB
      - payload: a parameter to pass to the operation being performed
    '''
    # print("Received event: " + json.dumps(event, indent=2))

    body = json.loads(event['body'])

    
    return {
        'statusCode': 200,
        'body': json.dumps(do_the_pokemon(body), indent=4),
        'headers': {
           'Content-Type': 'application/json', 
           'Access-Control-Allow-Origin': 'https://eis.github.io' 
       }
    }

class LocalFlask(Flask):
    def process_response(self, response):
        #Every response will be processed here first
        response.headers['Server'] = None
        super(LocalFlask, self).process_response(response)
        return(response)

app = LocalFlask(__name__)
app.debug = False

@app.route("/fights", methods=['GET', 'POST','OPTIONS'])
def fights():
    if not request.json:
        resp = app.make_response('{"msg":"No content"}')
    else:
        resp = app.make_response(json.dumps(do_the_pokemon(request.json), indent=4))
    resp.headers['Access-Control-Allow-Origin'] = 'https://eis.github.io'
    resp.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    resp.headers['Content-Type'] = 'application/json'
    return resp

if __name__ == '__main__':
    context = ('/etc/letsencrypt/live/slsh.iki.fi/cert.pem', 
        '/etc/letsencrypt/live/slsh.iki.fi/privkey.pem') #certificate and key files
    app.run(debug=False, ssl_context=context, host='0.0.0.0')


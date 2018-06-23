import http.client
import json
import sys

if len(sys.argv) < 2:
  sys.exit("Usage:\n{} AUTHTOKEN > pokemons.json".format(sys.argv[0]))

auth = sys.argv[1]

conn = http.client.HTTPSConnection('fight.pokebattler.com', 443)
# conn.set_debuglevel(1)
conn.putrequest('GET', '/secure/pokebox')
conn.putheader('User-Agent', sys.argv[0])
conn.putheader('Accept', 'application/json')
conn.putheader('Accept-Language','en-US,en;q=0.5')
conn.putheader('Referer','https://www.pokebattler.com/pokebox')
conn.putheader('X-Authorization','Bearer: {}'.format(auth))
conn.putheader('Origin','https://www.pokebattler.com')
conn.putheader('Cache-Control','max-age=0')
conn.endheaders()
r = conn.getresponse()
respbytes = r.read()
#print(respbytes.decode("utf-8"))
respjson = json.loads(respbytes.decode("utf-8"))['pokemon']

print(json.dumps(respjson, indent=4))

from flask import Flask
from flask import request

from fetch-fight-stats import *

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


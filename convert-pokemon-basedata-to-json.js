fs = require('fs');
eval(fs.readFileSync('pokemon-basedata.js')+'');
process.stdout.write(JSON.stringify(pokemon));
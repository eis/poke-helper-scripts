# Some helper scripts for poke battler

### Fetch the box - do your auth manually first to get the token

<pre>
$ python3 fetch-bokebattler-box.py AUTHTOKEN > pokemons.json
</pre>

### output as excel-friendly

<pre>
$ pip install pandas
$ python3 excel-pokebattler-box.py < pokemons.json
</pre>

### find out moves for any target pokemon
<pre>
$ python3 find-pokemon.py pikachu
PIKACHU
THUNDER_SHOCK_FAST - DISCHARGE
THUNDER_SHOCK_FAST - THUNDERBOLT
THUNDER_SHOCK_FAST - WILD_CHARGE
QUICK_ATTACK_FAST - DISCHARGE
QUICK_ATTACK_FAST - THUNDERBOLT
QUICK_ATTACK_FAST - WILD_CHARGE
THUNDER_SHOCK_FAST - SURF
QUICK_ATTACK_FAST - SURF
PRESENT_FAST - DISCHARGE
PRESENT_FAST - THUNDERBOLT
PRESENT_FAST - WILD_CHARGE
PRESENT_FAST - SURF
THUNDER_SHOCK_FAST - THUNDER
QUICK_ATTACK_FAST - THUNDER
</pre>

### put your pokemons to the test!

<pre>
$ pip install pandas
$ python3 fetch-fight-stats.py pikachu thunder_shock_fast discharge 4430 < pokemons.json

fetching for DRAGONITE (cp 3263)
          level        iv    cp moveset  power  effectiveCombatTime  overallRating
pokemon
dragonite  34.5  14/15/12  3263    dt/o  867.9                 20.6          409.1
</pre>

# giovanni

A CLI tool used to calculate the likelihood of a shiny Pokemon encounter for a
given number of resets, or simulate the distribution of required SRs for a given
generation of Pokemon.


### Encounter odds:

Compute the probability of encountering a shiny in Gen 4 with a single encounter:

```
$ python -m giovanni odds --gen 4 --verbose
[INFO] 2020-12-22 16:07:54 [giovanni.cli.odds] - Odds of shiny after 1 soft reset: 0.012%
```

The probability of encountering a shiny in Gen 6 with 5000 SRs and a shiny charm equipped:

```
$ python -m giovanni odds --gen 6 --soft_resets 5000 --charm
[INFO] 2020-12-22 16:07:57 [giovanni.cli.odds] - Odds of shiny after 5,000 soft resets: 91.301%
```

The odds of encountering a shiny starter in HG/SS after 2500 SRs:

```
$ python -m giovanni odds --gen 4 --soft_resets 2500 --swarm_size 3
[INFO] 2020-12-24 07:40:44 [giovanni.cli.odds] - Odds of shiny after 2,500 soft resets: 59.972%
```


### Montecarlo simulation:

A simulation of Gen 6 soft resets required to encounter a shiny:

```
$ python -m giovanni simulate --gen 6 -n 5000
simulation: 100%|████████████████████████████████████████████| 5000/5000 [00:13<00:00, 365.02it/s]
[INFO] 2020-12-22 15:53:43 [giovanni.cli.simulate] - Montecarlo simulation results --
Average     3980.136
Std Dev     3983.669
Max        32989.000
Min            1.000
Name: Required encounters (gen=6, num_trials=5000, swarm_size=1), dtype: float64
```

To simulate, e.g., SS/HG soft resets required to encounter a shiny starter use
the `swarm_size` argument:

```
python -m giovanni simulate --gen 4 -n 5000 --swarm_size 3
simulation: 100%|████████████████████████████████████████████| 5000/5000 [00:15<00:00, 329.87it/s]
[INFO] 2020-12-22 15:51:01 [giovanni.cli.simulate] - Montecarlo simulation results --
Average     2737.669
Std Dev     2717.707
Max        22760.000
Min            1.000
Name: Required encounters (gen=4, num_trials=5000, swarm_size=3), dtype: float64
```

### Notes

* No considerations are made around [shiny locks](https://pokemon-shiny-hunting.fandom.com/wiki/Shiny_Locks).
  Make sure that you are aware whether the 'Mon you're hunting can be found in shiny form.
  
* This project only covers the main titles in the game series. It does not cover offshoots or
  mobile games in the series.
  
* The current implementation only takes into account base shiny rates by generation (see **future work**)


### Future work

A list of things that would be cool to implement:

* Considerations around encounter method:
    * Wild/SR
    * Masuda
    * Chaining
    * Etc.
    
* Gen 8

## Installing

### Installing from PyPi:

giovanni is available on public PyPi:

```bash
$ pip install giovanni
```

### Get setup for local dev:

Set up by cloning and building from Git:

```bash
$ git clone https://github.com/tgsmith61591/giovanni.git
$ cd giovanni
$ make requirements lint-requirements testing-requirements
```

Run a quick test to make sure everything is copacetic:

```bash
$ make test
```

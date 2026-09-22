# max-profit-problem

Finds the most profitable mix of Theatres (T), Pubs (P) and Commercial Parks (C)
to build in `n` units of time. Only one property can be built at a time, and
each finished property earns money for every remaining unit of time.

| Property | Build time | Earnings per unit of time |
|---|---|---|
| Theatre | 5 | $1500 |
| Pub | 4 | $1000 |
| Commercial Park | 10 | $2000 |

## Run

```
python3 max_profit.py <time_units>
```

Example:

```
$ python3 max_profit.py 13
Time Unit: 13
Earnings: $16500
Solutions
1. T: 2 P: 0 C: 0
```

## Test

```
python3 -m unittest -v test_max_profit
```

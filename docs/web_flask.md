# Flask Web Routes

Example Flask apps are provided in `web_flask/`.

## 0-hello_route.py
- Routes:
  - `/` → "Hello HBNB!"

Run
```bash
python3 web_flask/0-hello_route.py
```

## 4-number_route.py
- Routes:
  - `/` → "Hello HBNB!"
  - `/hbnb` → "HBNB"
  - `/c/<text>` → "C <text>" (`_` replaced with space)
  - `/python[/<text>]` → default text "is cool"
  - `/number/<int:n>` → "<n> is a number"

Run
```bash
python3 web_flask/4-number_route.py
```

## 5-number_template.py
- Same as above, plus:
  - `/number_template/<int:n>` → renders template `5-number.html` with `n`

## Additional apps
- See `web_flask/6-number_odd_or_even.py`, `7-states_list.py`, `8-cities_by_states.py`, `9-states.py`, `10-hbnb_filters.py`, `100-hbnb.py` for more routes and teardown usage.

Notes
- All routes use `strict_slashes=False`.
- Apps typically run on host `0.0.0.0`, port `5000`.
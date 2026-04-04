# CLAUDE.md

## Project Overview

**gradestats** is a minimal Flask web application for computing and visualizing grade statistics. Instructors paste a list of numeric grades (one per line) into a form, and the app returns a bar chart with distribution buckets and a summary stats overlay.

Deployed at: `https://faculty.washington.edu/pisan/grade-stats/`

---

## Repository Structure

```
gradestats/
├── app.py                  # Main Flask application — all logic lives here
├── index.cgi               # CGI entry point for Apache/production deployment
├── .htaccess               # Apache mod_rewrite rules (routes all URLs to index.cgi)
├── templates/
│   └── input-grades.html   # Single HTML template: grade input form
└── pypackages/             # All Python dependencies vendored here (no pip install needed)
```

No database, no tests, no build step.

---

## Technology Stack

| Layer | Library | Version |
|---|---|---|
| Web framework | Flask | 2.2.2 |
| Templates | Jinja2 | 3.1.2 |
| Charting | Matplotlib | 3.6.2 |
| Numerics | NumPy | 1.23.4 |
| Image processing | Pillow | 9.3.0 |
| Stats | Python `statistics` stdlib | — |
| Production server | `wsgiref.handlers.CGIHandler` | stdlib |

All dependencies are vendored under `pypackages/` and added to `sys.path` at startup. There is no `requirements.txt` because no installation step is expected.

---

## Running the Application

### Development

```bash
python3 app.py
# Flask dev server starts on http://0.0.0.0:8088 with debug=True
```

Visit `http://localhost:8088/` in a browser.

### Production (Apache CGI)

Apache rewrites all requests to `index.cgi` via `.htaccess`. The CGI handler bridges WSGI ↔ CGI and adjusts `SCRIPT_NAME` so Flask URL routing works correctly under the `/pisan/grade-stats/` path prefix.

---

## Application Logic (`app.py`)

### Route

```
GET  /  → renders templates/input-grades.html (grade input form)
POST /  → processes grades, returns inline HTML with chart
```

### Call chain for POST

```
hello_world() → process_post() → plot_png() → create_bar_plot()
                                                    ├── get_dist_stats(data)
                                                    └── data_into_buckets(data)
```

### Key functions

| Function | Purpose |
|---|---|
| `hello_world()` | Flask route handler; dispatches GET/POST |
| `process_post()` | Builds response HTML string for POST |
| `plot_png()` | Renders the matplotlib figure to a base64 PNG `<img>` tag |
| `create_bar_plot()` | Creates the `Figure` with bar chart and stats text box |
| `get_dist_stats(data)` | Computes total, mean, median, mode, stdev, min, max |
| `data_into_buckets(data)` | Bins grades into `[<50, 50-59, 60-69, 70-79, 80-89, >=90, NaN]` |
| `isInt(s)` | Returns `True` if string `s` can be parsed as an integer |

### Data flow

1. `request.form['grades']` is split on `\n`; blank lines are stripped.
2. Non-integer entries (e.g. strings) fall into the **NaN** bucket and are excluded from numeric stats.
3. The chart is rendered server-side into a `BytesIO` buffer and base64-encoded for inline embedding — no static files are written.

---

## Conventions & Patterns

- **All logic in one file** (`app.py`). Do not split into modules unless the file grows substantially.
- **Inline HTML building** — `process_post()` returns a hand-built HTML string, not a rendered template. This is intentional for brevity; do not refactor to a template without good reason.
- **No OOP** — Everything is module-level functions. Keep it that way unless complexity demands classes.
- **Vendored dependencies** — Never add a `pip install` step. If a new dependency is needed, install it into `pypackages/` with `pip install --target=pypackages <pkg>`.
- **No tests** — The project has no test suite. If adding tests, use `pytest` and place them in a `tests/` directory.
- **`debug=True`** is set in the dev server run block. Do not change this in production; `index.cgi` bypasses that code path entirely.

---

## Deployment Notes

- The `.htaccess` `RewriteRule` hardcodes `/pisan/grade-stats/index.cgi/`. If the deployment path changes, update both `.htaccess` and the `SCRIPT_NAME` trimming logic in `index.cgi`.
- `index.cgi` strips its own filename from `SCRIPT_NAME` so Flask's `url_for('/')` resolves correctly under the subdirectory path.
- The `pypackages/` directory must be present on the server; it is committed to git.

---

## What Not to Do

- Do not add a database or session state — the app is intentionally stateless.
- Do not move business logic into the template; keep `input-grades.html` as a pure form.
- Do not add authentication — this is a public utility page.
- Do not change the port (8088) without updating any server configuration that references it.

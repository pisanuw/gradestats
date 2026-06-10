# Briefing

- Purpose: Flask CGI app for visualizing grade distributions; accepts a pasted list of decimal grades and returns a bar chart with summary statistics (mean, median, mode, stdev).
- Current scope: 134-line Flask app (app.py) + pure-function module (grades.py) + 24 pytest tests. Deployed via index.cgi on UW faculty web server using user-dir pip install.
- Key decisions: pypackages/ is gitignored; deploy step is `pip install -r requirements.txt -t pypackages/`. Pure grade functions live in grades.py (no Flask/matplotlib imports) so tests run on plain Python without vendored packages.
- Non-goals: Consolidating the four overlapping grade tools (gradestats, gradeplotter, grade-histogram-plotter, gradestatsreplit) -- deferred, requires separate decision.

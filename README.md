# gradestats

Flask app for visualizing grade distributions. Displays a bar chart and summary statistics (mean, median, mode, stdev) for a pasted list of decimal grades.

## Local development

```bash
pip install -r requirements.txt
python app.py
```

Open http://localhost:8088

## UW server deployment (CGI)

The UW server requires packages installed locally because it does not allow system-level installs:

```bash
pip install -r requirements.txt -t pypackages/
```

Then upload all files (including `pypackages/`) to the server. The `index.cgi` entry point adds `pypackages/` to `sys.path` at runtime.

## Tests

```bash
pip install pytest
pytest
```

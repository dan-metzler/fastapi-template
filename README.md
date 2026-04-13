# FastAPI Starter

A one-command scaffold for building web applications with Python. No JavaScript frameworks, no build tools, no Node.js. Just run the script and start building.

**Stack:**

- **FastAPI** — Python web server
- **Jinja2** — HTML templates
- **HTMX** — page interactivity without writing JavaScript
- **Bulma CSS** — clean, responsive styling
- **SQLAlchemy** — database support (SQLite, Postgres, MySQL)

---

## What You Need Before Starting

You need three things installed on your computer:

1. **Python 3.13 or newer** — [Download here](https://www.python.org/downloads/)
   - During install, check the box that says **"Add Python to PATH"**
   - Verify it works: open a terminal and type `python --version`

2. **Git** — [Download here](https://git-scm.com/downloads)
   - Used to download this repo to your computer

3. **pipx** — install it after Python is installed:
   ```shell
   pip install pipx
   pipx ensurepath
   ```
   Then **close and reopen your terminal** before continuing.

---

## Setup (Do This Once)

### Step 1 — Install the `uv` package manager

`uv` is a fast Python package manager used to set up your project's dependencies.

```shell
pipx install uv
```

Verify it works:

```shell
uv --version
```

> **Troubleshooting:** If you get `'uv' is not recognized`, run `pipx list` to find the install path, add that folder to your system's PATH environment variable, then close and reopen your terminal.

---

### Step 2 — Download this repo

```shell
git clone https://github.com/dan-metzler/fastapi-template.git
cd <folder_you_cloned_to>
```

---

## Creating a New Project

### Step 3 — Run the setup script

```shell
python create_project.py "<folder_where_project_goes>" "<project_name>"
```

- `<folder_where_project_goes>` — a folder that already exists on your computer
- `<project_name>` — the name of your app (letters, numbers, hyphens, underscores only — no spaces)

**Example:**

```shell
python create_project.py "C:\Users\YourName\Desktop" "MyWebApp"
```

This will create a folder at `C:\Users\YourName\Desktop\MyWebApp` with everything set up.

**What the script does automatically:**

- Creates a Python virtual environment (`.venv`) with all dependencies installed
- Downloads HTMX and Bulma CSS into your project (no internet needed at runtime)
- Copies the starter app template (routes, HTML templates, static files)
- Creates a `.gitignore` file

---

### Step 4 — Navigate into your new project

```shell
cd C:\Users\YourName\Desktop\MyWebApp
```

> You must be inside the `MyWebApp` folder (not the parent folder) to run the server.

---

### Step 5 — Activate the virtual environment

The virtual environment keeps your project's dependencies isolated from the rest of your computer.

**Windows (PowerShell):**

```shell
.\.venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**

```shell
.venv\Scripts\activate.bat
```

**Mac / Linux:**

```shell
source .venv/bin/activate
```

You'll know it's active when you see `(.venv)` at the start of your terminal prompt.

---

### Step 6 — Start the development server

```shell
uvicorn main:app --reload
```

Open your browser and go to: **http://localhost:8000**

You should see the starter page. The `--reload` flag means the server automatically restarts whenever you save a file.

---

## Project Structure

After running the script, your project folder looks like this:

```
MyWebApp/
├── main.py                        # Your app — routes live here
└── frontend/
    ├── templates/
    │   ├── base.html              # Base layout (navbar, footer, CSS/JS links)
    │   └── index.html             # Home page — extend base.html for new pages
    └── public/
        ├── css/
        │   ├── bulma.min.css      # Bulma CSS framework (downloaded at setup)
        │   └── custom.css         # Your custom styles go here
        └── js/
            └── htmx.min.js        # HTMX (downloaded at setup)
```

---

## How to Add a New Page

**1. Create a template** — add a file to `frontend/templates/`, e.g. `about.html`:

```html
{% extends "base.html" %} {% block title %}About{% endblock %} {% block content %}
<div class="container">
  <h1 class="title">About</h1>
  <p>This is the about page.</p>
</div>
{% endblock %}
```

**2. Add a route** — open `main.py` and add:

```python
@app.get("/about")
async def about(request: Request):
    return templates.TemplateResponse(request=request, name="about.html")
```

Visit **http://localhost:8000/about** — done.

---

## How HTMX Works

HTMX lets you update parts of a page without a full reload, using only HTML attributes.

**Example — button that loads content from the server:**

In your template:

```html
<button hx-get="/hello" hx-target="#result" hx-swap="innerHTML">Click me</button>
<div id="result"></div>
```

In `main.py`:

```python
from fastapi.responses import HTMLResponse

@app.get("/hello", response_class=HTMLResponse)
async def hello():
    return "<p>Hello from the server!</p>"
```

When the button is clicked, HTMX sends a request to `/hello` and puts the response HTML inside `#result`. No JavaScript needed.

---

## Stopping the Server

Press `Ctrl + C` in the terminal.

---

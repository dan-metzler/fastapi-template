import os
import sys
import shutil
import subprocess
import json
from urllib.request import urlopen
from pathlib import Path

def run_command(cmd, check=True):
    """Run a system command safely."""
    try:
        subprocess.run(cmd, check=check, shell=True)
    except subprocess.CalledProcessError:
        print(f"❌ Error running: {cmd}")
        sys.exit(1)

def find_npm():
    """
    Find npm executable in a cross-platform way.
    Returns path to npm or None if not found.
    """
    # Try system PATH first
    npm_path = shutil.which("npm")
    if npm_path:
        return Path(npm_path)
    return None


def create_project(project_name):
    root_folder = Path.cwd()
    project_root = root_folder / project_name
    project_root.mkdir(parents=True, exist_ok=True)

    # Step 1: Create virtual environment
    venv_path = root_folder / "venv"
    if not venv_path.exists():
        print("⚙️ Creating virtual environment...")
        run_command(f"{sys.executable} -m venv {venv_path}")
    else:
        print(f"✔️ Virtual environment already exists at {venv_path}")

    # Step 2: pip executable
    pip_executable = venv_path / ("Scripts/pip.exe" if os.name == "nt" else "bin/pip")

    # Step 3: requirements.txt
    requirements = """
fastapi[standard]
uvicorn[standard]
sqlalchemy
jinja2
python-dotenv
supabase
"""
    req_file = root_folder / "requirements.txt"
    req_file.write_text(requirements, encoding="utf-8")
    print("✔️ requirements.txt created")


    ####################################################################
    # Create Prettier RC file
    ####################################################################

    prettierrc_file_content = """
{
  "printWidth": 120,
  "tabWidth": 2,
  "useTabs": false,
  "semi": true,
  "singleQuote": false,
  "bracketSpacing": true,
  "arrowParens": "always",
  "trailingComma": "es5",
  "endOfLine": "lf",
  "htmlWhitespaceSensitivity": "css",
  "proseWrap": "preserve",
  "embeddedLanguageFormatting": "auto"
}
"""

    prettierrc_file = root_folder / ".prettierrc"
    prettierrc_file.write_text(prettierrc_file_content, encoding="utf-8")
    print("✔️ .prettierrc created")


    ####################################################################
    # Step 4: Install dependencies
    ####################################################################
    print("⚙️ Installing dependencies...")
    run_command(f"{pip_executable} install -r {req_file}")
    print("✔️ Dependencies installed")


    ####################################################################
    # Step 5: Create Folder structure
    ####################################################################
    dirs = [
        root_folder / ".vscode",
        project_root / "backend" / "database",
        project_root / "frontend" / "public" / "css",
        project_root / "frontend" / "public" / "imgs",
        project_root / "frontend" / "public" / "js",
        project_root / "frontend" / "templates" / "components",
        project_root / "frontend" / "templates" / "auth",
        project_root / "frontend" / "templates" / "pages",
        project_root / "tests",
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)

    ####################################################################
    # Step 6: Create Files
    ####################################################################
    files = [
        project_root / "backend" / "database" / "__init__.py",
        project_root / "backend" / "database" / "crud.py",
        project_root / "backend" / "database" / "models.py",
        project_root / "backend" / "database" / "schemas.py",
        project_root / "frontend" / "public" / "css" / "input.css",
        project_root / "frontend" / "public" / "css" / "output.css",
        project_root / "frontend" / "public" / "imgs" / "favicon.svg",
        project_root / "frontend" / "public" / "js" / "alpine.min.js",
        project_root / "frontend" / "public" / "js" / "htmx.min.js",
        project_root / "frontend" / "public" / "js" / "darkmode.js",
        project_root / "frontend" / "templates" / "auth" / "form_login.html",
        project_root / "frontend" / "templates" / "auth" / "form_resetpassword.html",
        project_root / "frontend" / "templates" / "auth" / "form_signup.html",
        project_root / "frontend" / "templates" / "pages" / "github.html",
        project_root / "frontend" / "templates" / "pages" / "page1.html",
        project_root / "frontend" / "templates" / "pages" / "page2.html",
        project_root / "frontend" / "templates" / "components" / "navbar.html",
        project_root / "frontend" / "templates" / "components" / "footer.html",
        project_root / "frontend" / "templates" / "_base.html",
        project_root / "frontend" / "templates" / "index.html",
        project_root / "tests" / "__init__.py",
        project_root / ".env",
        project_root / ".gitignore",
        project_root / "main.py",
        root_folder / ".vscode" / "settings.json",
    ]
    for f in files:
        if not f.exists():
            f.touch()


    ####################################################################
    # npm install flowbite
    ####################################################################
    npm_path = find_npm()
    if npm_path:
        try:
            subprocess.run(
                [str(npm_path), "install", "flowbite"],
                cwd=project_root,
                check=True
            )
            print(f"✔️ [SUCCESS] Installed Flowbite using {npm_path}")
        except subprocess.CalledProcessError as e:
            print(f"❌ [ERROR] npm install failed: {e}")
    else:
        print("❌ [ERROR] npm not found on this system. Please install Node.js.")

    # flowbite.min.js copy to frontend/public/js
    src_dir = project_root / "node_modules" / "flowbite" / "dist"
    dest_dir = project_root / "frontend" / "public" / "js"

    # make sure destination exists
    dest_dir.mkdir(parents=True, exist_ok=True)

    # files to copy
    files = ["flowbite.min.js", "flowbite.min.js.map"]

    for fname in files:
        src = src_dir / fname
        dest = dest_dir / fname
        if src.exists():
            shutil.copy2(src, dest)
            print(f"✔️ [SUCCESS] Copied {src} -> {dest}")
        else:
            print(f"[WARNING] {src} not found")


    ####################################################################
    # install htmx link form https://cdn.jsdelivr.net/npm/htmx.org@2.0.6/dist/htmx.min.js to frontend/public/js
    ####################################################################
    install_path = project_root / "frontend" / "public" / "js" / "htmx.min.js"
    install_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with urlopen("https://cdn.jsdelivr.net/npm/htmx.org@2.0.6/dist/htmx.min.js") as r:
            data = r.read()
            install_path.write_bytes(data)
        print(f"✔️ [SUCCESS] Downloaded htmx ({len(data)} bytes) to {install_path}")
    except Exception as e:
        print(f"❌ [ERROR] Failed to download htmx: {e}")


    ####################################################################
    # install tailwindcss standalone executable
    ####################################################################
    tailwindcss_install_path = project_root / "tailwindcss.exe"
    url = "https://github.com/tailwindlabs/tailwindcss/releases/download/v4.1.12/tailwindcss-windows-x64.exe"

    try:
        with urlopen(url) as r:
            data = r.read()
            tailwindcss_install_path.write_bytes(data)
        print(f"✔️ [SUCCESS] Downloaded TailwindCSS ({len(data)} bytes) to {tailwindcss_install_path}")
    except Exception as e:
        print(f"❌ [ERROR] Failed to download TailwindCSS: {e}")


    ####################################################################
    # set main.py content
    ####################################################################
    main_py_content = """
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn

# 1. Creates an instance of the FastAPI class.
# This app object represents your entire web application.
# 2. Registers routes and middleware.
# Whenever you use decorators like @app.get("/...") or @app.post("/..."), you’re attaching routes (endpoints) to this app.
# 3. Passed to the ASGI server.
# When you run your project with uvicorn main:app, Uvicorn looks for app inside main.py and runs it.
app = FastAPI()

# MOUNT STATIC FOLDER AND DEFINE TEMPLATES DIRECTORY
app.mount('/static', StaticFiles(directory='frontend/public'), name='static')
templates = Jinja2Templates(directory='frontend/templates')


#####################################
# INDEX / HOME ROUTE
#####################################
@app.get('/', name='home', response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})

#####################################
# AUTENTICATION ROUTES
#####################################
@app.get('/login', name='login', response_class=HTMLResponse)
async def get_login(request: Request):
    return templates.TemplateResponse('auth/form_login.html', {'request' : request})

@app.get('/signup', name='signup', response_class=HTMLResponse)
async def get_signup(request: Request):
    return templates.TemplateResponse('auth/form_signup.html', {'request' : request})

@app.get('/resetpassword', name='resetpassword', response_class=HTMLResponse)
async def get_resetpassword(request: Request):
    return templates.TemplateResponse('auth/form_resetpassword.html', {'request' : request})

#####################################
# GENRAL ROUTES
#####################################
@app.get('/github', name='github', response_class=HTMLResponse)
async def get_github(request: Request):
    return templates.TemplateResponse('pages/github.html', {'request' : request})

@app.get('/page1', name='page1', response_class=HTMLResponse)
async def get_page1(request: Request):
    return templates.TemplateResponse('pages/page1.html', {'request' : request})

@app.get('/page2', name='page2', response_class=HTMLResponse)
async def get_page2(request: Request):
    return templates.TemplateResponse('pages/page2.html', {'request' : request})



# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# RUN (MIGHT NEED TO CUSTOMIZE FOR DEV / PROD)
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000, reload=True)
"""
    (project_root / "main.py").write_text(main_py_content, encoding="utf-8")




    ####################################################################
    # set favicon.svg content
    ####################################################################
    favicon_svg_content = """
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="100%" height="100%" viewBox="0 0 1406 1811" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" xmlns:serif="http://www.serif.com/" style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:2;">
    <g transform="matrix(5.55556,0,0,5.55556,-6408.21,-2925.27)">
        <g id="Logo-Official" serif:id="Logo Official" transform="matrix(1,0,0,1,-841.373,0)">
            <g transform="matrix(0.874068,0.874068,-1.1422,1.1422,870.686,-1948.6)">
                <rect x="2143.68" y="526.549" width="80.898" height="123.815" style="fill:url(#_Linear1);"/>
            </g>
            <g transform="matrix(0.874068,0.874068,-1.1422,1.1422,898.169,-1834.82)">
                <rect x="2143.68" y="526.549" width="80.898" height="123.815" style="fill:url(#_Linear2);"/>
            </g>
            <g transform="matrix(0.18,-0,-0,0.18,1994.85,526.549)">
                <use xlink:href="#_Image3" x="21" y="539.762" width="1012px" height="322px"/>
            </g>
            <g transform="matrix(0.18,-0,-0,0.18,1994.85,526.549)">
                <use xlink:href="#_Image4" x="373.5" y="1002.41" width="1010px" height="238px"/>
            </g>
            <g transform="matrix(0.0161303,1.23601,-1.61517,0.0210785,3050.34,-2040.42)">
                <path d="M2217.16,523.118L2237.73,627.897L2179.79,671.097L2159.28,566.269L2217.16,523.118Z" style="fill:rgb(0,189,255);fill-opacity:0.44;"/>
            </g>
        </g>
    </g>
    <defs>
        <linearGradient id="_Linear1" x1="0" y1="0" x2="1" y2="0" gradientUnits="userSpaceOnUse" gradientTransform="matrix(-40.0473,124.051,-324.211,-61.2925,2183.73,526.313)"><stop offset="0" style="stop-color:rgb(0,189,255);stop-opacity:1"/><stop offset="1" style="stop-color:rgb(0,14,142);stop-opacity:1"/></linearGradient>
        <linearGradient id="_Linear2" x1="0" y1="0" x2="1" y2="0" gradientUnits="userSpaceOnUse" gradientTransform="matrix(41.1489,-123.751,161.714,31.4892,2183.55,650.388)"><stop offset="0" style="stop-color:rgb(0,189,255);stop-opacity:1"/><stop offset="1" style="stop-color:rgb(0,14,142);stop-opacity:1"/></linearGradient>
        <image id="_Image3" width="1012px" height="322px" xlink:href="data:image/png;base64,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"/>
        <image id="_Image4" width="1010px" height="238px" xlink:href="data:image/png;base64,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"/>
    </defs>
</svg>
"""
    (project_root / "frontend" / "public" / "imgs" / "favicon.svg").write_text(favicon_svg_content, encoding="utf-8")


    ####################################################################
    # darkmode.js copy to frontend/public/js
    ####################################################################
    darkmode_js_content = """
var themeToggleDarkIcon = document.getElementById('theme-toggle-dark-icon');
var themeToggleLightIcon = document.getElementById('theme-toggle-light-icon');

// Change the icons inside the button based on previous settings
if (localStorage.getItem('color-theme') === 'dark' || (!('color-theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    themeToggleLightIcon.classList.remove('hidden');
} else {
    themeToggleDarkIcon.classList.remove('hidden');
}

var themeToggleBtn = document.getElementById('theme-toggle');

themeToggleBtn.addEventListener('click', function() {

    // toggle icons inside button
    themeToggleDarkIcon.classList.toggle('hidden');
    themeToggleLightIcon.classList.toggle('hidden');

    // if set via local storage previously
    if (localStorage.getItem('color-theme')) {
        if (localStorage.getItem('color-theme') === 'light') {
            document.documentElement.classList.add('dark');
            localStorage.setItem('color-theme', 'dark');
        } else {
            document.documentElement.classList.remove('dark');
            localStorage.setItem('color-theme', 'light');
        }

    // if NOT set via local storage previously
    } else {
        if (document.documentElement.classList.contains('dark')) {
            document.documentElement.classList.remove('dark');
            localStorage.setItem('color-theme', 'light');
        } else {
            document.documentElement.classList.add('dark');
            localStorage.setItem('color-theme', 'dark');
        }
    }
    
});
"""
    (project_root / "frontend" / "public" / "js" / "darkmode.js").write_text(darkmode_js_content, encoding="utf-8")


    ####################################################################
    # set _base.html content
    ####################################################################
    base_html_content = """
<!doctype html>
<html lang="en">
  <head>
    <script>
      // On page load or when changing themes, best to add inline in `head` to avoid FOUC
      if (
        localStorage.getItem("color-theme") === "dark" ||
        (!("color-theme" in localStorage) && window.matchMedia("(prefers-color-scheme: dark)").matches)
      ) {
        document.documentElement.classList.add("dark");
      } else {
        document.documentElement.classList.remove("dark");
      }
    </script>

    <!-- Character encoding -->
    <meta charset="UTF-8" />

    <!-- Viewport for responsiveness -->
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />

    <!-- Page title -->
    <title>{{ title if title else 'Home' }}</title>

    <!-- Description for SEO -->
    <meta name="description" content="{{ description if description else 'MyApp is a modern web application.' }}" />

    <!-- Keywords (optional, minor SEO impact) -->
    <meta name="keywords" content="fastapi, web app, python, frontend" />

    <!-- Open Graph / Social sharing -->
    <meta property="og:title" content="{{ title if title else 'MyApp | Home' }}" />
    <meta
      property="og:description"
      content="{{ description if description else 'MyApp is a modern web application.' }}"
    />
    <meta property="og:type" content="website" />
    <meta property="og:url" content="{{ request.url }}" />
    <meta property="og:image" content="{{ url_for('static', path='imgs/og-image.png') }}" />

    <!-- Favicon -->
    <link rel="icon" href="{{ url_for('static', path='imgs/favicon.svg') }}" type="image/x-icon" />

    <!-- CSS -->
    <link rel="stylesheet" href="{{ url_for('static', path='css/output.css') }}" />

    <!-- Optional: Google Fonts -->
    <!-- <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto&display=swap"> -->
  </head>
  <body class="dark:bg-gray-900">
    {% include 'components/navbar.html' %} {% block content %}{% endblock %} {% include 'components/footer.html' %}

    <!-- Import the flowbite javascript file -->
    <script src="{{ url_for('static', path='js/flowbite.min.js') }}"></script>
    <script src="{{ url_for('static', path='js/darkmode.js') }}"></script>
  </body>
</html>
"""
    (project_root / "frontend" / "templates" / "_base.html").write_text(base_html_content, encoding="utf-8")


    ####################################################################
    # set index.html content
    ####################################################################
    index_html_content = """
{% extends '_base.html' %}
{% block content %}
<section class="bg-white dark:bg-gray-900">
    <div class="py-8 px-4 mx-auto max-w-screen-xl lg:py-16">
        <div class="bg-gray-100 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-8 md:p-12 mb-8">
            <a href="#" class="bg-blue-100 text-blue-800 text-xs font-medium inline-flex items-center px-2.5 py-0.5 rounded-md dark:bg-gray-700 dark:text-blue-400 mb-2">
                Core Technologies
            </a>
            <h1 class="text-gray-900 dark:text-gray-300 text-3xl md:text-5xl font-extrabold mb-2"><span class="text-transparent bg-clip-text bg-gradient-to-r from-green-400 via-green-500 to-green-600">FastAPI</span>, <span class="text-transparent bg-clip-text bg-gradient-to-r from-red-400 via-red-500 to-red-600">Jinja2</span>, <span class="text-transparent bg-clip-text bg-gradient-to-r from-gray-400 via-gray-500 to-gray-600">HTMX</span>, <span class="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-blue-500 to-blue-600">Flowbite</span> <span class="text-xl">&</span> <span class="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-cyan-500 to-cyan-600">AlpineJS</span></h1>
            <p class="text-lg font-normal text-gray-500 dark:text-gray-400 mb-6">This project makes spinning up a web application fast and effortless by providing a ready-to-use foundation. 
    Instead of starting from scratch, you get preconfigured tools and a clean structure so you can focus on building features right away.</p>
        </div>
        <div class="grid md:grid-cols-2 gap-8">
            <div class="bg-gray-100 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-8 md:p-12">
                <a href="#" class="bg-green-100 text-green-800 text-xs font-medium inline-flex items-center px-2.5 py-0.5 rounded-md dark:bg-gray-700 dark:text-green-400 mb-2">
                    Authentication
                </a>
                <h2 class="text-gray-900 dark:text-gray-300 text-3xl font-extrabold mb-2"><span class="text-transparent bg-clip-text bg-gradient-to-r from-amber-400 via-amber-500 to-amber-600">JWT</span> <span class="text-xl">&</span> <span class="text-transparent bg-clip-text bg-gradient-to-r from-slate-300 via-slate-400 to-slate-500">OAuth</span></h2>
                <p class="text-lg font-normal text-gray-500 dark:text-gray-400 mb-4">Static websites are now used to bootstrap lots of websites and are becoming the basis for a variety of tools that even influence both web designers and developers.</p>
            </div>
            <div class="bg-gray-100 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-8 md:p-12">
                <a href="#" class="bg-purple-100 text-purple-800 text-xs font-medium inline-flex items-center px-2.5 py-0.5 rounded-md dark:bg-gray-700 dark:text-purple-400 mb-2">
                    Backend
                </a>
                <h2 class="text-gray-900 dark:text-gray-300 text-3xl font-extrabold mb-2"><span class="text-transparent bg-clip-text bg-gradient-to-r from-emerald-500 via-emerald-600 to-emerald-700">Supabase</span>, <span class="text-transparent bg-clip-text bg-gradient-to-r from-rose-300 via-rose-400 to-rose-500">Pydantic</span>, <span class="text-xl">&</span> <span class="text-transparent bg-clip-text bg-gradient-to-r from-slate-400 via-slate-500 to-slate-600">SQL</span><span class="text-transparent bg-clip-text bg-gradient-to-r from-red-500 via-red-600 to-red-700">Alchemy</span> </h2>
                <p class="text-lg font-normal text-gray-500 dark:text-gray-400 mb-4">Static websites are now used to bootstrap lots of websites and are becoming the basis for a variety of tools that even influence both web designers and developers.</p>
            </div>
        </div>
    </div>
</section>
{% endblock %}
"""
    (project_root / "frontend" / "templates" / "index.html").write_text(index_html_content, encoding="utf-8")


    ####################################################################
    # set navbar.html content
    ####################################################################
    navbar_html_content = """
<nav class="bg-white border-gray-200 dark:bg-gray-900">
  <div class="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4">
    <!-- Logo -->
    <a href="{{ url_for('home') }}" class="flex items-center space-x-3 rtl:space-x-reverse">
      <img src="{{ url_for('static', path='imgs/favicon.svg') }}" class="h-8" alt="Webstrides Logo" />
      <span class="self-center text-2xl font-semibold whitespace-nowrap dark:text-white">Webstrides</span>
    </a>

    <!-- Right-side controls: theme toggle + hamburger -->
    <div class="flex items-center space-x-2 md:order-2">
      <!-- Theme toggle (always visible) -->
      <button
        id="theme-toggle"
        type="button"
        class="text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 hover:cursor-pointer focus:outline-none focus:ring-4 focus:ring-gray-200 dark:focus:ring-gray-700 rounded-lg text-sm p-2"
      >
        <svg id="theme-toggle-dark-icon" class="hidden w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
          <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z"></path>
        </svg>
        <svg id="theme-toggle-light-icon" class="hidden w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
          <path
            d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 
                   4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 
                   1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 
                   0 11-1.414-1.414l.707-.707a1 1 0 
                   011.414 0zM17 11a1 1 0 100-2h-1a1 
                   1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 
                   0 11-2 0v-1a1 1 0 011-1zM5.05 
                   6.464A1 1 0 106.465 5.05l-.708-.707a1 
                   1 0 00-1.414 1.414l.707.707zm1.414 
                   8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 
                   1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 
                   1 0 000 2h1z"
            fill-rule="evenodd"
            clip-rule="evenodd"
          ></path>
        </svg>
      </button>

      <!-- Hamburger menu (small screens only) -->
      <button
        data-collapse-toggle="navbar-default"
        type="button"
        class="inline-flex items-center p-2 w-10 h-10 justify-center text-sm text-gray-500 rounded-lg md:hidden hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200 dark:text-gray-400 dark:hover:bg-gray-700 dark:focus:ring-gray-600"
        aria-controls="navbar-default"
        aria-expanded="false"
      >
        <span class="sr-only">Open main menu</span>
        <svg class="w-5 h-5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 17 14">
          <path
            stroke="currentColor"
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M1 1h15M1 7h15M1 13h15"
          />
        </svg>
      </button>
    </div>

    <!-- Collapsible nav links -->
    <div class="hidden w-full md:block md:w-auto md:order-1" id="navbar-default">
      <ul
        class="font-medium flex flex-col md:flex-row md:space-x-8 md:items-center sm:items-left mt-4 md:mt-0 border border-gray-100 rounded-lg bg-gray-50 md:border-0 md:bg-white dark:bg-gray-800 md:dark:bg-gray-900 dark:border-gray-700 p-4 md:p-0"
      >
        <li>
          {% if request.scope['path'] == '/' %}
          <a
            href="{{ url_for('home') }}"
            class="block py-2 px-3 text-blue-500 rounded-sm hover:bg-gray-100 md:hover:bg-transparent md:hover:text-blue-700 md:p-0 dark:text-blue-500 md:dark:hover:text-blue-500 dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent"
            >Home</a
          >
          {% else %}
          <a
            href="{{ url_for('home') }}"
            class="block py-2 px-3 text-gray-900 rounded-sm hover:bg-gray-100 md:hover:bg-transparent md:hover:text-blue-700 md:p-0 dark:text-white md:dark:hover:text-blue-500 dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent"
            >Home</a
          >
          {% endif %}
        </li>

        <li>
          {% if request.scope['path'] == '/github' %}
          <a
            href="{{ url_for('github') }}"
            class="block py-2 px-3 text-blue-500 rounded-sm hover:bg-gray-100 md:hover:bg-transparent md:hover:text-blue-700 md:p-0 dark:text-blue-500 md:dark:hover:text-blue-500 dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent"
            >GitHub</a
          >
          {% else %}
          <a
            href="{{ url_for('github') }}"
            class="block py-2 px-3 text-gray-900 rounded-sm hover:bg-gray-100 md:hover:bg-transparent md:hover:text-blue-700 md:p-0 dark:text-white md:dark:hover:text-blue-500 dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent"
            >GitHub</a
          >
          {% endif %}
        </li>

        <li>
          {% if request.scope['path'] == '/page1' %}
          <a
            href="{{ url_for('page1') }}"
            class="block py-2 px-3 text-blue-500 rounded-sm hover:bg-gray-100 md:hover:bg-transparent md:hover:text-blue-700 md:p-0 dark:text-blue-500 md:dark:hover:text-blue-500 dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent"
            >Page1</a
          >

          {% else %}
          <a
            href="{{ url_for('page1') }}"
            class="block py-2 px-3 text-gray-900 rounded-sm hover:bg-gray-100 md:hover:bg-transparent md:hover:text-blue-700 md:p-0 dark:text-white md:dark:hover:text-blue-500 dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent"
            >Page1</a
          >

          {% endif %}
        </li>

        <li>
          {% if request.scope['path'] == '/page2' %}
          <a
            href="{{ url_for('page2') }}"
            class="block py-2 px-3 text-blue-500 rounded-sm hover:bg-gray-100 md:hover:bg-transparent md:hover:text-blue-700 md:p-0 dark:text-blue-500 md:dark:hover:text-blue-500 dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent"
            >Page2</a
          >

          {% else %}
          <a
            href="{{ url_for('page2') }}"
            class="block py-2 px-3 text-gray-900 rounded-sm hover:bg-gray-100 md:hover:bg-transparent md:hover:text-blue-700 md:p-0 dark:text-white md:dark:hover:text-blue-500 dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent"
            >Page2</a
          >
          {% endif %}
        </li>

        <li>
          {% if request.scope['path'] == '/login' %}

          <a href="{{ url_for('signup') }}">
            <button
              type="button"
              class="hidden md:block text-white bg-gradient-to-r from-green-500 via-green-600 to-green-700 hover:bg-gradient-to-br hover:cursor-pointer focus:ring-4 focus:outline-none focus:ring-green-300 dark:focus:ring-green-800 shadow-lg shadow-green-500/50 dark:shadow-lg dark:shadow-green-800/80 font-medium rounded-lg text-sm px-5 py-2 w-30"
            >
              Sign up
            </button>
          </a>

          {% else %}
          <!-- Button: visible on md+ -->
          <a href="{{ url_for('login') }}">
            <button
              type="button"
              class="hidden md:block text-white bg-gradient-to-r from-sky-500 via-sky-600 to-sky-700 hover:bg-gradient-to-br hover:cursor-pointer focus:ring-4 focus:outline-none focus:ring-sky-300 dark:focus:ring-sky-800 shadow-lg shadow-sky-500/50 dark:shadow-lg dark:shadow-sky-800/80 font-medium rounded-lg text-sm px-5 py-2 w-30"
            >
              Login
            </button>
          </a>
          {% endif %} {% if request.scope['path'] == '/login' %}

          <!-- A tag: visible only on small screens -->
          <a
            href="{{ url_for('signup') }}"
            class="block md:hidden text-white bg-gradient-to-r from-green-500 to-green-600 hover:bg-gradient-to-bl focus:ring-4 focus:outline-none focus:ring-green-300 dark:focus:ring-green-800 font-medium rounded-sm py-2 px-3 text-left"
          >
            Sign up
          </a>

          {% else %}

          <!-- A tag: visible only on small screens -->
          <a
            href="{{ url_for('login') }}"
            class="block md:hidden text-white bg-gradient-to-r from-cyan-500 to-blue-500 hover:bg-gradient-to-bl focus:ring-4 focus:outline-none focus:ring-cyan-300 dark:focus:ring-cyan-800 font-medium rounded-sm py-2 px-3 text-left"
          >
            Login
          </a>

          {% endif %}
        </li>
      </ul>
    </div>
  </div>
</nav>
"""
    (project_root / "frontend" / "templates" / "components" / "navbar.html").write_text(navbar_html_content, encoding="utf-8")


    ####################################################################
    # footer
    ####################################################################
    footer_html_content = """
<footer class="bg-white rounded-lg shadow-sm m-4 dark:bg-gray-800 md:w-[75%] w-[94%] mx-auto">
    <div class="w-full mx-auto max-w-screen-xl p-4 md:flex md:items-center md:justify-between">
      <span class="text-sm text-gray-500 sm:text-center dark:text-gray-400">© 2025 <a href="#" class="hover:underline">Webstrides™</a>. All Rights Reserved.
    </span>
    <ul class="flex flex-wrap items-center mt-3 text-sm font-medium text-gray-500 dark:text-gray-400 sm:mt-0">
        <li>
            <a href="#" class="hover:underline me-4 md:me-6">About</a>
        </li>
        <li>
            <a href="#" class="hover:underline me-4 md:me-6">Privacy Policy</a>
        </li>
        <li>
            <a href="#" class="hover:underline me-4 md:me-6">Licensing</a>
        </li>
        <li>
            <a href="#" class="hover:underline">Contact</a>
        </li>
    </ul>
    </div>
</footer>
"""
    (project_root / "frontend" / "templates" / "components" / "footer.html").write_text(footer_html_content, encoding="utf-8")


    ####################################################################
    # set all form.html auth page content
    ####################################################################

    form_login_content = """
{% extends '_base.html' %} {% block content %}
<section class="bg-gray-50 dark:bg-gray-900">
  <div class="flex flex-col items-center justify-center px-6 py-8 mx-auto md:h-screen lg:py-0">
    <div
      class="w-full bg-white rounded-lg shadow dark:border md:mt-0 sm:max-w-md xl:p-0 dark:bg-gray-800 dark:border-gray-700"
    >
      <div class="p-6 space-y-4 md:space-y-6 sm:p-8">
        <h1 class="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl dark:text-white">
          Welcome back
        </h1>

        <!-- Social login buttons -->
        <div class="flex justify-between">
          <button
            type="button"
            class="text-white bg-gray-600 hover:bg-gray-600/90 focus:ring-4 focus:outline-none focus:ring-gray-600/50 font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center dark:focus:ring-gray-600/55"
          >
            <svg
              class="w-4 h-4 mr-2"
              viewBox="0 0 256 262"
              version="1.1"
              xmlns="http://www.w3.org/2000/svg"
              xmlns:xlink="http://www.w3.org/1999/xlink"
              preserveAspectRatio="xMidYMid"
            >
              <g>
                <path
                  d="M255.878,133.451 C255.878,122.717 255.007,114.884 253.122,106.761 L130.55,106.761 L130.55,155.209 L202.497,155.209 C201.047,167.249 193.214,185.381 175.807,197.565 L175.563,199.187 L214.318,229.21 L217.003,229.478 C241.662,206.704 255.878,173.196 255.878,133.451"
                  fill="#4285F4"
                />
                <path
                  d="M130.55,261.1 C165.798,261.1 195.389,249.495 217.003,229.478 L175.807,197.565 C164.783,205.253 149.987,210.62 130.55,210.62 C96.027,210.62 66.726,187.847 56.281,156.37 L54.75,156.5 L14.452,187.687 L13.925,189.152 C35.393,231.798 79.49,261.1 130.55,261.1"
                  fill="#34A853"
                />
                <path
                  d="M56.281,156.37 C53.525,148.247 51.93,139.543 51.93,130.55 C51.93,121.556 53.525,112.853 56.136,104.73 L56.063,103 L15.26,71.312 L13.925,71.947 C5.077,89.644 0,109.517 0,130.55 C0,151.583 5.077,171.455 13.925,189.152 L56.281,156.37"
                  fill="#FBBC05"
                />
                <path
                  d="M130.55,50.479 C155.064,50.479 171.6,61.068 181.029,69.917 L217.873,33.943 C195.245,12.91 165.798,0 130.55,0 C79.49,0 35.393,29.301 13.925,71.947 L56.136,104.73 C66.726,73.253 96.027,50.479 130.55,50.479"
                  fill="#EB4335"
                />
              </g>
            </svg>

            Login with Google
          </button>
          <button
            type="button"
            class="text-white bg-black hover:bg-gray-900 focus:ring-4 focus:outline-none focus:ring-gray-400 font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center dark:bg-[#050708] dark:hover:bg-gray-700 dark:focus:ring-gray-500"
          >
            <svg
              class="w-5 h-5 mr-2 -ml-1"
              aria-hidden="true"
              xmlns="http://www.w3.org/2000/svg"
              fill="currentColor"
              viewBox="0 0 384 512"
            >
              <path
                d="M318.7 268.7c-.2-36.7 16.4-64.4 50-84.8-18.8-26.9-47.2-41.7-84.7-44.6-35.5-2.8-74.3 20.7-88.5 20.7-15 0-49.4-19.7-76.4-19.7C63.3 141.2 4 184.8 4 273.5q0 39.3 14.4 81.2c12.8 36.7 59 126.7 107.2 125.2 25.2-.6 43-17.9 75.8-17.9 31.8 0 48.3 17.9 76.4 17.9 48.6-.7 90.4-82.5 102.6-119.3-65.2-30.7-61.7-90-61.7-91.9zm-56.6-164.2c27.3-32.4 24.8-61.9 24-72.5-24.1 1.4-52 16.4-67.9 34.9-17.5 19.8-27.8 44.3-25.6 71.9 26.1 2 49.9-11.4 69.5-34.3z"
              />
            </svg>
            Login with Apple
          </button>
        </div>

        <div class="flex items-center justify-between">
          <span class="w-full border border-gray-300 dark:border-gray-700"></span>
          <span class="px-2 text-gray-500 dark:text-gray-400">or</span>
          <span class="w-full border border-gray-300 dark:border-gray-700"></span>
        </div>

        <!-- Login form -->
        <form class="space-y-4 md:space-y-6" action="{{ url_for('login') }}" method="post">
          <div>
            <label for="email" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Email</label>
            <input
              type="email"
              name="email"
              id="email"
              placeholder="Enter your email"
              class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white"
              required
            />
          </div>
          <div>
            <label for="password" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Password</label>
            <input
              type="password"
              name="password"
              id="password"
              placeholder="••••••••"
              class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white"
              required
            />
          </div>
          <div class="flex items-center justify-between">
            <div class="flex items-center">
              <input
                id="remember"
                type="checkbox"
                class="w-4 h-4 border border-gray-300 rounded bg-gray-50 focus:ring-3 focus:ring-blue-300 dark:border-gray-600 dark:bg-gray-700 dark:focus:ring-blue-600"
              />
              <label for="remember" class="ml-2 text-sm text-gray-600 dark:text-gray-300">Remember me</label>
            </div>
            <a
              href="{{ url_for('resetpassword') }}"
              class="text-sm font-medium text-blue-600 hover:underline dark:text-blue-500"
              >Forgot password?</a
            >
          </div>
          <button
            type="submit"
            class="w-full text-white bg-blue-600 hover:bg-blue-700 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
          >
            Login to your account
          </button>
          <p class="text-sm font-light text-gray-600 dark:text-gray-400">
            Don't have an account yet?
            <a href="{{ url_for('signup') }}" class="font-medium text-green-600 hover:underline dark:text-green-500"
              >Sign up here</a
            >
          </p>
        </form>
      </div>
    </div>
  </div>
</section>
{% endblock %}
"""
    (project_root / "frontend" / "templates" / "auth" / "form_login.html").write_text(form_login_content, encoding="utf-8")

    form_resetpassword_content = """
{% extends '_base.html' %} {% block content %}
<section class="bg-gray-50 dark:bg-gray-900">
  <div class="flex flex-col items-center justify-center px-6 py-8 mx-auto md:h-screen lg:py-0">
    <div
      class="w-full p-6 bg-white rounded-lg shadow dark:border md:mt-0 sm:max-w-md dark:bg-gray-800 dark:border-gray-700 sm:p-8"
    >
      <!-- Title -->
      <h1 class="mb-2 text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl dark:text-white">
        Forgot your password?
      </h1>
      <p class="font-light text-gray-600 dark:text-gray-400">
        Don't worry! Enter your email and we'll send you a reset code.
      </p>
      <!-- Form -->
      <form class="mt-4 space-y-4 lg:mt-5 md:space-y-5" action="#" method="post">
        <!-- Email -->
        <div>
          <label for="email" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"> Your email </label>
          <input
            type="email"
            name="email"
            id="email"
            placeholder="name@company.com"
            required
            class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
          />
        </div>
        <!-- Terms -->
        <div class="flex items-start">
          <div class="flex items-center h-5">
            <input
              id="terms"
              type="checkbox"
              required
              class="w-4 h-4 border border-gray-300 rounded bg-gray-50 focus:ring-3 focus:ring-blue-300 dark:bg-gray-700 dark:border-gray-600 dark:focus:ring-blue-600 dark:ring-offset-gray-800"
            />
          </div>
          <div class="ml-3 text-sm">
            <label for="terms" class="font-light text-gray-600 dark:text-gray-300">
              I accept the
              <a href="#" class="font-medium text-blue-600 hover:underline dark:text-blue-500">
                Terms and Conditions
              </a>
            </label>
          </div>
        </div>
        <!-- Submit -->
        <button
          type="submit"
          class="w-full text-white bg-blue-600 hover:bg-blue-700 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
        >
          Reset password
        </button>
      </form>
    </div>
  </div>
</section>
{% endblock %}

"""
    (project_root / "frontend" / "templates" / "auth" / "form_resetpassword.html").write_text(form_resetpassword_content, encoding="utf-8")

    form_signup_content = """
{% extends '_base.html' %} {% block content %}
<section class="bg-gray-50 dark:bg-gray-900">
  <div class="flex flex-col items-center justify-center px-6 py-8 mx-auto md:h-screen lg:py-0">
    <div
      class="w-full bg-white rounded-lg shadow dark:border md:mt-0 sm:max-w-7xl xl:p-0 dark:bg-gray-800 dark:border-gray-700"
    >
      <div class="grid grid-cols-1 md:grid-cols-2">
        <!-- Left side: Signup form -->
        <div class="p-6 space-y-4 md:space-y-6 sm:p-8">
          <h1 class="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl dark:text-white">
            Your Best Work Starts Here
          </h1>
          <!-- Social login buttons -->
          <div class="flex gap-2">
            <button
              type="button"
              class="text-white bg-gray-600 hover:bg-gray-600/90 focus:ring-4 focus:outline-none focus:ring-gray-600/50 font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center w-1/2"
            >
              <svg
                class="w-4 h-4 mr-2"
                viewBox="0 0 256 262"
                version="1.1"
                xmlns="http://www.w3.org/2000/svg"
                xmlns:xlink="http://www.w3.org/1999/xlink"
                preserveAspectRatio="xMidYMid"
              >
                <g>
                  <path
                    d="M255.878,133.451 C255.878,122.717 255.007,114.884 253.122,106.761 L130.55,106.761 L130.55,155.209 L202.497,155.209 C201.047,167.249 193.214,185.381 175.807,197.565 L175.563,199.187 L214.318,229.21 L217.003,229.478 C241.662,206.704 255.878,173.196 255.878,133.451"
                    fill="#4285F4"
                  />
                  <path
                    d="M130.55,261.1 C165.798,261.1 195.389,249.495 217.003,229.478 L175.807,197.565 C164.783,205.253 149.987,210.62 130.55,210.62 C96.027,210.62 66.726,187.847 56.281,156.37 L54.75,156.5 L14.452,187.687 L13.925,189.152 C35.393,231.798 79.49,261.1 130.55,261.1"
                    fill="#34A853"
                  />
                  <path
                    d="M56.281,156.37 C53.525,148.247 51.93,139.543 51.93,130.55 C51.93,121.556 53.525,112.853 56.136,104.73 L56.063,103 L15.26,71.312 L13.925,71.947 C5.077,89.644 0,109.517 0,130.55 C0,151.583 5.077,171.455 13.925,189.152 L56.281,156.37"
                    fill="#FBBC05"
                  />
                  <path
                    d="M130.55,50.479 C155.064,50.479 171.6,61.068 181.029,69.917 L217.873,33.943 C195.245,12.91 165.798,0 130.55,0 C79.49,0 35.393,29.301 13.925,71.947 L56.136,104.73 C66.726,73.253 96.027,50.479 130.55,50.479"
                    fill="#EB4335"
                  />
                </g>
              </svg>
              Sign up with Google
            </button>
            <button
              type="button"
              class="text-white bg-black hover:bg-gray-900 focus:ring-4 focus:outline-none focus:ring-gray-400 font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center w-1/2 dark:bg-[#050708] dark:hover:bg-gray-700 dark:focus:ring-gray-500"
            >
              <svg
                class="w-5 h-5 mr-2 -ml-1"
                xmlns="http://www.w3.org/2000/svg"
                fill="currentColor"
                viewBox="0 0 384 512"
              >
                <path
                  d="M318.7 268.7c-.2-36.7 16.4-64.4 50-84.8-18.8-26.9-47.2-41.7-84.7-44.6-35.5-2.8-74.3 20.7-88.5 20.7-15 0-49.4-19.7-76.4-19.7C63.3 141.2 4 184.8 4 273.5q0 39.3 14.4 81.2c12.8 36.7 59 126.7 107.2 125.2 25.2-.6 43-17.9 75.8-17.9 31.8 0 48.3 17.9 76.4 17.9 48.6-.7 90.4-82.5 102.6-119.3-65.2-30.7-61.7-90-61.7-91.9zm-56.6-164.2c27.3-32.4 24.8-61.9 24-72.5-24.1 1.4-52 16.4-67.9 34.9-17.5 19.8-27.8 44.3-25.6 71.9 26.1 2 49.9-11.4 69.5-34.3z"
                />
              </svg>
              Sign up with Apple
            </button>
          </div>

          <div class="flex items-center justify-between">
            <span class="w-full border border-gray-300 dark:border-gray-700"></span>
            <span class="px-2 text-gray-500 dark:text-gray-400">or</span>
            <span class="w-full border border-gray-300 dark:border-gray-700"></span>
          </div>
          <!-- Signup form -->
          <form class="space-y-4 md:space-y-6" action="{{ url_for('signup') }}" method="post">
            <div>
              <label for="name" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
                >What should we call you?</label
              >
              <input
                type="text"
                name="name"
                id="name"
                placeholder="e.g. Bonnie Green"
                class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg block w-full p-2.5 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white"
                required
              />
            </div>
            <div>
              <label for="email" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Your email</label>
              <input
                type="email"
                name="email"
                id="email"
                placeholder="name@company.com"
                class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg block w-full p-2.5 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white"
                required
              />
            </div>
            <div>
              <label for="password" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
                >Your password</label
              >
              <input
                type="password"
                name="password"
                id="password"
                placeholder="••••••••"
                class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg block w-full p-2.5 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white"
                required
              />
            </div>
            <!-- Terms and updates -->
            <div class="flex items-start">
              <div class="flex items-center h-5">
                <input
                  id="terms"
                  name="terms"
                  type="checkbox"
                  required
                  class="w-4 h-4 border border-gray-300 rounded bg-gray-50 focus:ring-3 focus:ring-blue-300 dark:border-gray-600 dark:bg-gray-700 dark:focus:ring-blue-600"
                />
              </div>
              <label for="terms" class="ml-2 text-sm font-light text-gray-600 dark:text-gray-400">
                By signing up, you are creating a Webstrides account, and you agree to Webstride's
                <a href="#" class="font-medium text-blue-600 hover:underline dark:text-blue-500">Terms of Use</a> and
                <a href="#" class="font-medium text-blue-600 hover:underline dark:text-blue-500">Privacy Policy</a>.
              </label>
            </div>

            <div class="flex items-start">
              <div class="flex items-center h-5">
                <input
                  id="updates"
                  name="updates"
                  type="checkbox"
                  class="w-4 h-4 border border-gray-300 rounded bg-gray-50 focus:ring-3 focus:ring-blue-300 dark:border-gray-600 dark:bg-gray-700 dark:focus:ring-blue-600"
                />
              </div>
              <label for="updates" class="ml-2 text-sm font-light text-gray-600 dark:text-gray-400">
                Email me about product updates and resources.
              </label>
            </div>

            <button
              type="submit"
              class="w-full text-white bg-blue-600 hover:bg-blue-700 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
            >
              Create an account
            </button>
            <p class="text-sm font-light text-gray-600 dark:text-gray-400">
              Already have an account?
              <a href="{{ url_for('login') }}" class="font-medium text-sky-600 hover:underline dark:text-sky-500"
                >Login here</a
              >
            </p>
          </form>
        </div>
        <!-- Right side: Marketing block -->
        <div class="hidden md:flex flex-col justify-center px-8 py-12 bg-blue-600 rounded-r-lg">
          <a href="#" class="flex items-center mb-6 text-white text-2xl font-semibold">
            <svg class="w-8 h-8 mr-2" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 0L24 22H0L12 0z" />
            </svg>
            Webstrides
          </a>
          <h2 class="mb-4 text-3xl font-extrabold leading-tight tracking-tight text-white">
            Explore the world's leading design portfolios.
          </h2>
          <p class="mb-6 text-lg text-gray-100">
            Millions of designers and agencies showcase their portfolio work on Webstrides — the home to the world's
            best design and creative professionals.
          </p>
          <div class="flex items-center space-x-2">
            <img
              class="w-10 h-10 rounded-full"
              src="https://flowbite.s3.amazonaws.com/blocks/marketing-ui/avatars/bonnie-green.png"
              alt="avatar 1"
            />
            <img
              class="w-10 h-10 rounded-full"
              src="https://flowbite.s3.amazonaws.com/blocks/marketing-ui/avatars/jese-leos.png"
              alt="avatar 2"
            />
            <img
              class="w-10 h-10 rounded-full"
              src="https://flowbite.s3.amazonaws.com/blocks/marketing-ui/avatars/michael-gough.png"
              alt="avatar 3"
            />
            <span class="text-sm text-white">Over <strong>15.7k</strong> Happy Customers</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
{% endblock %}
"""
    (project_root / "frontend" / "templates" / "auth" / "form_signup.html").write_text(form_signup_content, encoding="utf-8")

    ####################################################################
    # set all general page content
    ####################################################################

    github_html_content = """
{% extends '_base.html' %} {% block content %}
<section class="flex justify-center mt-10">
  <div class="p-6 bg-white border border-gray-200 rounded-lg shadow-sm dark:bg-gray-800 dark:border-gray-700">
    <a href="#">
      <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">
        Checkout the project on GitHub
      </h5>
    </a>
    <p class="mb-3 font-normal text-gray-700 dark:text-gray-400">
      Here are the biggest enterprise technology acquisitions of 2021 so far, in reverse chronological order.
    </p>
    <a
      href="#"
      class="inline-flex items-center px-3 py-2 text-sm font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
    >
      Read more
      <svg
        class="rtl:rotate-180 w-3.5 h-3.5 ms-2"
        aria-hidden="true"
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 14 10"
      >
        <path
          stroke="currentColor"
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M1 5h12m0 0L9 1m4 4L9 9"
        />
      </svg>
    </a>
  </div>
</section>
{% endblock %}

"""
    (project_root / "frontend" / "templates" / "pages" / "github.html").write_text(github_html_content, encoding="utf-8")

    page1_html_content = """
{% extends '_base.html' %} {% block content %}
<section class="bg-white dark:bg-gray-900">
  <div class="flex justify-center max-w-screen-xl px-4 py-8 mx-auto lg:gap-8 xl:gap-0 lg:py-16 lg:grid-cols-12">
    <h1
      class="max-w-2xl mb-4 text-4xl font-extrabold tracking-tight leading-none md:text-5xl xl:text-6xl dark:text-white"
    >
      Page 1
    </h1>
  </div>
</section>
{% endblock %}
"""
    (project_root / "frontend" / "templates" / "pages" / "page1.html").write_text(page1_html_content, encoding="utf-8")

    page2_html_content = """
{% extends '_base.html' %} {% block content %}
<section class="bg-white dark:bg-gray-900">
  <div class="flex justify-center max-w-screen-xl px-4 py-8 mx-auto lg:gap-8 xl:gap-0 lg:py-16 lg:grid-cols-12">
    <h1
      class="max-w-2xl mb-4 text-4xl font-extrabold tracking-tight leading-none md:text-5xl xl:text-6xl dark:text-white"
    >
      Page 2
    </h1>
  </div>
</section>
{% endblock %}
"""
    (project_root / "frontend" / "templates" / "pages" / "page2.html").write_text(page2_html_content, encoding="utf-8")



    ####################################################################
    # set input.css content
    ####################################################################
    input_css_content = """
@import "tailwindcss";

@custom-variant dark (&:where(.dark, .dark *));

@import "flowbite/src/themes/default";
@plugin "flowbite/plugin";
@source "../node_modules/flowbite";
"""
    (project_root / "frontend" / "public" / "css" / "input.css").write_text(input_css_content, encoding="utf-8")

    ####################################################################
    # set vscode settings.json content
    ####################################################################
    vscode_settingsjson_content = """
{
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.formatOnSave": true,
  "[html]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[jinja-html]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  }
}
"""
    (root_folder / ".vscode" / "settings.json").write_text(vscode_settingsjson_content, encoding="utf-8")


    package_json_path = project_root / "package.json"

    # Load the existing package.json
    with package_json_path.open("r", encoding="utf-8") as f:
        package_data = json.load(f)

    # Add the scripts section if it doesn't exist
    package_data.setdefault("scripts", {})
    package_data["scripts"]["dev"] = "npx @tailwindcss/cli -i ./frontend/public/css/input.css -o ./frontend/public/css/output.css --watch"

    # Write the updated JSON back
    with package_json_path.open("w", encoding="utf-8") as f:
        json.dump(package_data, f, indent=2)

    print("✔️ Added 'scripts' section to package.json")


    # vscode settings.json workspace settings

    print("🎉 Project setup complete!")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("project_name", help="Name of the project")
    args = parser.parse_args()
    create_project(args.project_name)


# Example Usage: 
# python create_project.py myapp
import os
import sys
import shutil
import subprocess
import json
import re
from urllib.request import urlopen
from pathlib import Path

def run_command(cmd, check=True):
    """
    Run a system command safely with better error logging.
    Shows stdout/stderr if the command fails.
    """
    try:
        result = subprocess.run(
            cmd,
            check=check,
            shell=True,
            text=True,
            capture_output=True
        )
        # If you want to see output live, print it here
        if result.stdout:
            print(result.stdout.strip())
        return result
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error running command: {cmd}")
        if e.stdout:
            print(f"--- STDOUT ---\n{e.stdout.strip()}")
        if e.stderr:
            print(f"--- STDERR ---\n{e.stderr.strip()}")
        sys.exit(e.returncode)
    except FileNotFoundError:
        print(f"\n❌ Command not found: {cmd}")
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

def ensure_python_version(min_version=(3, 13)):
    """
    Ensure the running Python interpreter is >= min_version.
    min_version should be a tuple like (3, 13).
    """
    if sys.version_info < min_version:
        raise RuntimeError(
            f"❌ Python {min_version[0]}.{min_version[1]} or higher is required. "
            f"❌ Current version: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        )
    print(f"✅ Python version OK: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} | SystemExecutablePath: {sys.executable}")

def display_banner():
    print(r"""
    ____           __              _       __                       __      __     
   / __/___ ______/ /_____ _____  (_)     / /____  ____ ___  ____  / /___ _/ /____ 
  / /_/ __ `/ ___/ __/ __ `/ __ \/ /_____/ __/ _ \/ __ `__ \/ __ \/ / __ `/ __/ _ \
 / __/ /_/ (__  ) /_/ /_/ / /_/ / /_____/ /_/  __/ / / / / / /_/ / / /_/ / /_/  __/
/_/  \__,_/____/\__/\__,_/ .___/_/      \__/\___/_/ /_/ /_/ .___/_/\__,_/\__/\___/ 
                        /_/                              /_/                       
""")

def create_project(project_folderpath, project_name):

    ####################################################################
    # display banner, check python version installed, define root folder
    ####################################################################
    display_banner()
    print("=================================================================================")
    ensure_python_version()
    print("=================================================================================")
    print()


    clone_directory = Path.cwd()

    # input validation
    input_path = Path(project_folderpath)


    if not input_path.exists():
        sys.exit(f"The input project_folderpath does not exist: {project_folderpath}")
        
    if not re.match(r'^[A-Za-z0-9_-]+$', project_name):
      sys.exit("Error: project name can only contain letters, numbers, hyphens, and underscores. No spaces allowed.")

    print(f"✔ project_name   : {project_name}")
    print(f"✔ project_folder : {project_folderpath}")    
    os.chdir(project_folderpath)
    print("✔ Set Current directory:", Path.cwd())


    root_folder = input_path

    ####################################################################
    # Step 1: Create virtual environment using uv
    ####################################################################

    run_command('uv init --bare')

    ####################################################################
    # Create the project name folder
    ####################################################################
    project_root = root_folder / project_name
    project_root.mkdir(parents=True, exist_ok=True)


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
    print("✔ .prettierrc created")


    ####################################################################
    # Step 4: Install dependencies
    ####################################################################
    req_file = clone_directory / "requirements.txt"
    run_command(f"uv add -r {req_file}")
    print("✔ Dependencies installed")


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
                [str(npm_path), "install", "flowbite", "--no-fund", "--no-audit"],
                cwd=project_root,
                check=True
            )
            print(f"✔ Success: Installed Flowbite using {npm_path}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error: npm install failed: {e}")
    else:
        print("❌ Error: npm not found on this system. Please install Node.js.")

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
            print(f"✔ Success: Copied {src} -> {dest}")
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
        print(f"✔ Success: Downloaded htmx ({len(data)} bytes) to {install_path}")
    except Exception as e:
        print(f"❌ Error: Failed to download htmx: {e}")


    ####################################################################
    # install tailwindcss standalone executable
    ####################################################################
    tailwindcss_install_path = project_root / "tailwindcss.exe"
    url = "https://github.com/tailwindlabs/tailwindcss/releases/download/v4.1.12/tailwindcss-windows-x64.exe"

    try:
        with urlopen(url) as r:
            data = r.read()
            tailwindcss_install_path.write_bytes(data)
        print(f"✔ Success: Downloaded TailwindCSS ({len(data)} bytes) to {tailwindcss_install_path}")
    except Exception as e:
        print(f"❌ Error: Failed to download TailwindCSS: {e}")


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
<svg width="100%" height="100%" viewBox="0 0 254 326" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" xmlns:serif="http://www.serif.com/" style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:2;">
    <g transform="matrix(1,0,0,1,-1153.48,-526.549)">
        <g id="Logo-Official" serif:id="Logo Official" transform="matrix(1,0,0,1,-841.373,0)">
            <g transform="matrix(0.874068,0.874068,-1.1422,1.1422,870.686,-1948.6)">
                <rect x="2143.68" y="526.549" width="80.898" height="123.815" style="fill:url(#_Linear1);"/>
            </g>
            <g transform="matrix(0.874068,0.874068,-1.1422,1.1422,898.169,-1834.82)">
                <rect x="2143.68" y="526.549" width="80.898" height="123.815" style="fill:url(#_Linear2);"/>
            </g>
            <g transform="matrix(1,-0,-0,1,1994.85,526.549)">
                <use xlink:href="#_Image3" x="3" y="96.937" width="183px" height="58px"/>
            </g>
            <g transform="matrix(1,-0,-0,1,1994.85,526.549)">
                <use xlink:href="#_Image4" x="66.45" y="179.734" width="183px" height="45px"/>
            </g>
            <g transform="matrix(0.0161303,1.23601,-1.61517,0.0210785,3050.34,-2040.42)">
                <path d="M2217.16,523.118L2237.73,627.897L2179.79,671.097L2159.28,566.269L2217.16,523.118Z" style="fill:rgb(0,189,255);fill-opacity:0.44;"/>
            </g>
        </g>
    </g>
    <defs>
        <linearGradient id="_Linear1" x1="0" y1="0" x2="1" y2="0" gradientUnits="userSpaceOnUse" gradientTransform="matrix(-40.0473,124.051,-324.211,-61.2925,2183.73,526.313)"><stop offset="0" style="stop-color:rgb(0,189,255);stop-opacity:1"/><stop offset="1" style="stop-color:rgb(0,14,142);stop-opacity:1"/></linearGradient>
        <linearGradient id="_Linear2" x1="0" y1="0" x2="1" y2="0" gradientUnits="userSpaceOnUse" gradientTransform="matrix(41.1489,-123.751,161.714,31.4892,2183.55,650.388)"><stop offset="0" style="stop-color:rgb(0,189,255);stop-opacity:1"/><stop offset="1" style="stop-color:rgb(0,14,142);stop-opacity:1"/></linearGradient>
        <image id="_Image3" width="183px" height="58px" xlink:href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAALcAAAA6CAYAAADyQMiZAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAGnElEQVR4nO2da3ajSgyEi8z8zmKzkCw2Cwj3B9MXuShJ3YDfqnM4/TT0jD+XhSB4Qqn0TPr8ntyxn68Zn98Tfr5mAPAnlkr3VgRypp+v+e+JSymVjukIzEIFd+m+8oEeAX1WnQV36fYaB7r1S4g9Fdyl20gDzX0Z3BNywP8fL7hL19E+mD/EaxqsHvgzHGcvuEvnKQd6ckpvftZmF5+9iaXSuGKgJ/ggs0tb9/X2OZs5MHW1lXOXdmgLtAWVnXoSfVm9tWcqgS3Yv84qK89d6tTnt+e0rc4ureqA7+QMsTqO1S8undy2AZRzl1iXrqxAYzg/aIxhtuOzGIczrlwbWMOODyxAt9K+DkDB/b6Kc82e01qgPbeO3JtB9dyajw1cunRzak4NlnO/leJL2l72gl2Z3Tlrt7pyYj4+O7RyarumX2q3OQx/wf0y6oPYthXQ2WZhZxfPjmfhVXOj9GATAyyzJADqxqmn1DjEtp45M8PLQFuH5mNkcbSNlS2kyqVV3YYjvEnAC+5H1TGIbd2Liz03nuDH1AruSF6oYdd36bh5DlvBfZkp+Xc/d8F9b50HsS0ZQoY1Apk3iDqgIWzj6v4PTtVtQwkRNyOG26YAl+0f2EDBfTtdB2LPkYF+oNtc76SQxRdULNQqRIicGPCBVvMt4NFx3MWX9iq/2b4H4gzmvUB7UKt9coaCwVMu3LIYXM6iHTk0kvHwJNKsqZx7l8ZcmPsyiM8GmvuBbYbD+/dYh2xtYAszzzkKtFfqMYI6+0eVgCOhhG2rEzzVjsDOgLYneza8+KB9eSeEymVtCABq8xhfClehxwjE6Ohb5IANFNyLrh8Pc7kXaC7Va1S/3X9PNkKdwAFbsHuB9tq8np52CLTVe4UljwNxBrTX5wGt9mnrCjiVbbAQ62zEFmKG3JZZH5K+RZ0ws17TuW8H8VGgAZ2243l8S2nbZqcNxJkHD2yGG9jCDWzDGHU8rqv2pXZC7Om54b4PxCNw9+zHtr1xntfqs5jnZRi80CJzcGALte3jumpf6mSIPT1HWPJYEPcA3Xs8LhlW68wM7ERlG1MZDXZrBt3LfAA+0Kq96kYAR3oc5759jlj17XVlb33Rmr3Xz6btOXMre0IPBW8UanDd7n+rB4DY0+3hvn2OWI2NxsUZxKo9U5udtvf/Pso4qAsnWSjiAa3aqx4YYk/Xg/txcsS9c9XxojV6GgHXe636+ldQZnAroO18gI/1hBB7Og73uRAfiYt7x3kdEdAs741XMbCC1MqD2CsjRwb1R1mNpf1CEHsag7v/MVgZPEcgHomFz4J4tM1j3vEyh/bc17uAArd8A5hZOdxboHuAuRfEWcxuFQFqwZiwBcZ7/STq3nHtvtVJorovI7pgwqHHWwJtFcO9gn2kPCuM2BsP90KcjXn74mNzH0PP++m9e872qf0senOgrTQU2z/v5w0n1Lm8VijhAdsz7sXFNq7O1Oap9Jq3ngjicudObd+cS7fmTd2NhqTu9fF4vK5VvU4cfW2PAh3Jzvc+DN4xszCD5y8qoLvkXaFkoD+whVs9jAVByXXVblJvXgZB5IK2zjF0BLTn0B7EHpAcevSWqwroYV2+aYtrK7B589xb7/d8iI8CzcfLIJ6o7WkU3nLnK2p9M9dwxLr0B4A/iOHe7kvLeyOPOrGqq+My5BHQwBZq79/C7Wj93txFBfSpWsISnRVhoP+Yfu9NB/ZBfMSVQW3OTETrs+3ItbMPDq9XlXpNBfTVZGPu6ASS/5C0KXoD9zpwNO61IwCBbTjBH84IwN4Pa9a3qGC+mdQJpQo5er5aj4YRWYjBfT1Aq9KqfTCyb6BsLeXOD6i/nb/9N2N9qib3t3KvK9sy6wNWqFU4kYUkPRCr/mxNBfQDKvpjhQY04GcL9riyLaO6bfO3CLu2ipdHcuc9ayqYn0wK7ganff5xFmufBbFVA1S5dOTaXLfH8FJ5PessoJ9MCwRrfrv1qTx205Gvax+GBkr/L2JxXbU9FcxvIAv32vZPspoyaHOIrcZ/s7BnvreO3mzIogL6aaUu4vS6HzAKsdW+e8NVO9P4B7GAfgmpy+9j2gPCvl+X3RNy9LQL5hdVDMzn93TqG3/897971tIXIhXQL69xp96jPqizfqWemHpRwfx2ut5DecYf4dCjfpiBAvrNdesnTvVeDd03XjCXjK4D954TU60Y1oK5FOjcmLsf6pE/XlhVMJcGdK8HYfZDWkCXdurxnvJaMJdO0nVSgb3hSYFcuqL+A6Jc7WsIIjV2AAAAAElFTkSuQmCC"/>
        <image id="_Image4" width="183px" height="45px" xlink:href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAALcAAAAtCAYAAADsk/q6AAAACXBIWXMAAA7EAAAOxAGVKw4bAAAD6ElEQVR4nO2cwXKjMAyGlbbnfdg+yD5s7hv2QByEkGTZ2MSQ/5thbMtso8M3qgzp3giA0fnz9xa+9/47pWn8HwHQG1/iiKsvsen+O0FucDxlEt+cvcTExpfgP+WZARCkjcQ3JSZZSZ3mkBvsI98PRyT2YjflZySS0A9tD3KDGH0l1oS29hKpWj+I6Os58uqNyg0E9a0EX0uJS+SVMS2fidatyIPdj5774+krsVx788g+h4v9T9l7AbmvTp9DXbQSl8itjXwuq/TmAMnmOFBeijEl9mLaaOU7PWNcbOt6AbnPxnES7xXaG72cE1o1TgdIeW0Fv//iacmwvEfimgrstRLWmjM5a3lotORePyl5voL3PhQcwVgSl7QUufw0vD5ZjnKexOaC89h84bslB3Psi47Wh7tcfpJoJc4JzWPyeoj5fC8Tmwg9d1vKv/hTInGPqmx9npcz0VZgHouMkbm17x4iI8kDj/c+I87tlx7qWrYSadwrdMnPJVmxE5Dbo63Ee/ri6L7Mw6vKkr0S1+x7Yy42Y4hNBLlnzv2M2JtrWD1xrzaCnLWXj7V2heZ8ltznljjXs3NyhzprrJXYimmfo+VnxWaCMkuuKff5XnTUHOqI+koc73nzMWu9plJii3PLPdYz4pJYLj9JrpWQsZZC5z7Py29LY4E9ziH3WBKXytujEte0CZeV2GIcuT/nRYfXb/Y83HmjN7dynhlAYovj5e77oiONtUJ7MSvHnoc6LVYj76Ultugn97lfdHhzjZw8JcJG973Rm2vrhRNKbLFf7nEer0X3vTy0NaelxNF7rbXMIbJeuJDEFmVy2yIfKXFJG/GudqJFVc7FvJwXPkBii7zcW6Ejv7pL5dViJfJqMmt5cXpKXHK4y8Ws9ZoPltjCl3sRe8/YqgK3aCX42pKrZVXOfZ6Xnw4kDqNLoUvNL2owt2JyP5/vTESYEiH3Hu6iOW2BwE3YyrIWW15fSowycxmz1n5eM16/GRlbVmBIPDhriXSxv2iRWo7yXnLG7ee1l7hHBYbEJ0X7SxxZpZPc3yJuSS3n2pqTkwcSgyoWueeqrbUh37QV3KvUFnslrhHaWsscIusFSHwKZrnXj/t4teZXktyq1kS+ID16YUgMTHhb4h0geY/N8X6l10pc0o7kcrDWayDxJfH++p3LHKmKLXrhSB8MiUGIH6Ul0Zho/v8hrDakRVXmozfX1gsQGDyRlXuiReAkNNG6x7aqKSQGQ6G1JUnOVKm58PyektGba+sFSAwqmaVdHgOmmPYcO1HSB0Ni8DZ45U4V2pPTikNiMBxLVY4dLCWQGAyL9d2SOJAYnJIa2QEYhP/LZwn2L32npAAAAABJRU5ErkJggg=="/>
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

    print("✔ Added 'scripts' section to package.json")

    print("🎉 Project setup complete!")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Create a new project")
    parser.add_argument("project_folderpath", help="Folder where the project will be created")
    parser.add_argument("project_name", help="Name of the project")
    args = parser.parse_args()
    # Call your function
    create_project(args.project_folderpath, args.project_name)


# Example Usage: 
# python create_project.py myapp
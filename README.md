# 🚀 FastAPI Starter Setup Script

This repository provides a script that **automates the setup** of a modern FastAPI web application with the following stack:

- **FastAPI** – High-performance Python web framework
- **Jinja2** – Templating engine for server-rendered HTML
- **Tailwind CSS** – Utility-first CSS framework
- **Flowbite** – Tailwind UI components
- **HTMX** – Modern HTML-over-the-wire interactivity
- **Supabase** – Authentication, database, and storage backend
- **Alpine.js** – Lightweight JavaScript framework

Perfect for building **scalable, full-stack web apps** quickly with a clean developer experience.

---

## ✅ TODO / In Progress

- [x] Add "uv" instead of "pip" for dependency management
- [] Add Authentication from supabase
- [] Add User and Admin authorization with routes
- [] Google Analytics Dashboard
- [] SMTP Email Functionality

---

## 📦 Features

- 🔧 One-command setup for project scaffolding
- ⚡ FastAPI backend with Jinja2 templating out of the box
- 🎨 Tailwind + Flowbite integration for styling and UI components
- 🔄 HTMX for dynamic interactivity without heavy JavaScript
- 🛠 Supabase client configured for database + auth
- 🪶 Alpine.js for lightweight frontend state management

---

## 🚀 Getting Started

### 1. Install [pipx](https://pypi.org/project/pipx/)

```shell
pip install pipx
```

> If installing from PyPI, we recommend installing uv into an isolated environment, e.g., with pipx

### 2. Installing [UV](https://docs.astral.sh/uv/) package manager

```shell
pipx install uv
```

### 2. Verify UV installation

```shell
uv
```

> if you run into error [The term 'uv' is not recognized as a name of a cmdlet, function, script file, or executable program.] run **pipx list** to see where uv is installed and add the folder path to system evironment variables. Then, open a new terminal (or restart VS Code) and try again.

### 3. Clone the repo

```shell
git clone https://github.com/your-username/fastapi-starter-setup.git
cd fastapi-starter-setup
```

### 4. Create a project

```shell
python create_project.py <new_project_folderpath> <project_name>


# Example :
python .\create_project.py "C:\Users\User\Desktop\my-new-project" "AppNameExample"
```

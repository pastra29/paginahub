from fastapi import FastAPI, Form, Request, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from datetime import datetime
import os
import shutil

app = FastAPI()
templates = Jinja2Templates(directory=".")
# Configura FastAPI para servir archivos estáticos desde la carpeta 'static'
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory=".")

# Crear un directorio para las fotos (si no existe)
if not os.path.exists("static/photos"):
    os.makedirs("static/photos")

# Función para guardar la foto
def save_photo(photo: UploadFile):
    photo_path = os.path.join("static/photos", photo.filename)
    with open(photo_path, "wb") as buffer:
        shutil.copyfileobj(photo.file, buffer)
    return photo.filename

# Crear un directorio para las fotos (si no existe)
if not os.path.exists("static/photos"):
    os.makedirs("static/photos")

# Función para cargar textos según el idioma
def load_texts(lang: str):
    if lang == "en":
        return {
            "title": "Curriculum Form",
            "welcome": "Welcome",
            "enter_name": "Please enter your name",
            "submit": "Submit",
            "personal_info": "Personal Information",
            "full_name": "Full Name",
            "address": "Address",
            "phone": "Phone",
            "email": "Email",
            "dob": "Date of Birth",
            "photo": "Profile Photo",  # Nueva pregunta
            "professional_profile": "Professional Profile",
            "work_experience": "Work Experience",
            "education": "Education",
            "skills": "Skills",
            "certifications": "Certifications",
            "languages": "Languages",
            "references": "References",
            "curriculum_of": "Curriculum of",
            "age": "Age",
            "back": "Go Back",
        }
    # Español por defecto
    return {
        "title": "Formulario de Currículum",
        "welcome": "Bienvenido",
        "enter_name": "Por favor, ingresa tu nombre",
        "submit": "Enviar",
        "personal_info": "Información Personal",
        "full_name": "Nombre Completo",
        "address": "Dirección",
        "phone": "Teléfono",
        "email": "Correo Electrónico",
        "dob": "Fecha de Nacimiento",
        "photo": "Foto de Perfil",  # Nueva pregunta
        "professional_profile": "Perfil Profesional",
        "work_experience": "Experiencia Laboral",
        "education": "Educación",
        "skills": "Habilidades",
        "certifications": "Certificaciones",
        "languages": "Idiomas",
        "references": "Referencias",
        "curriculum_of": "Currículum de",
        "age": "Edad",
        "back": "Regresar",
    }

# Función para cargar la foto
def save_photo(photo: UploadFile):
    photo_path = os.path.join("static/photos", photo.filename)
    with open(photo_path, "wb") as buffer:
        shutil.copyfileobj(photo.file, buffer)
    return photo.filename

# Función para calcular la edad a partir de la fecha de nacimiento
def calculate_age(birthdate: str) -> int:
    birthdate = datetime.strptime(birthdate, "%Y-%m-%d")
    today = datetime.today()
    age = today.year - birthdate.year
    if today.month < birthdate.month or (today.month == birthdate.month and today.day < birthdate.day):
        age -= 1
    return age

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, lang: str = "es"):
    texts = load_texts(lang)
    return templates.TemplateResponse("index.html", {"request": request, "texts": texts, "lang": lang, "name": None})

@app.post("/", response_class=HTMLResponse)
async def submit_name(request: Request, name: str = Form(...), lang: str = "es"):
    texts = load_texts(lang)
    return templates.TemplateResponse("index.html", {"request": request, "texts": texts, "lang": lang, "name": name})
@app.get("/edit", response_class=HTMLResponse)
async def edit_curriculum(request: Request):
    # Aquí puedes obtener los datos del currículum del usuario, por ejemplo de la base de datos o sesión
    # Este es un ejemplo ficticio
    user_data = {
        "name": "Juan Pérez",
        "full_name": "Juan Pérez Gómez",
        "address": "Calle Ficticia 123",
        "phone": "123456789",
        "email": "juan@email.com",
        "profile": "Soy un desarrollador web con experiencia en Python y FastAPI.",
        "work_experience": "Desarrollador Backend en XYZ.",
        "education": "Ingeniería en Sistemas.",
        "skills": "Python, FastAPI, HTML, CSS.",
        "certifications": "Certificado en Desarrollo Web.",
        "languages": "Español, Inglés",
        "references": "Referencia 1: Nombre, Teléfono",
        "dob": "1990-01-01",  # Fecha de nacimiento
    }
    return templates.TemplateResponse("index.html", {"request": request, **user_data})

@app.post("/edit", response_class=HTMLResponse)
async def update_curriculum(
    request: Request,
    name: str = Form(...),
    full_name: str = Form(...),
    address: str = Form(...),
    phone: str = Form(...),
    email: str = Form(...),
    profile: str = Form(...),
    work_experience: str = Form(...),
    education: str = Form(...),
    skills: str = Form(...),
    certifications: str = Form(...),
    languages: str = Form(...),
    references: str = Form(...),
    dob: str = Form(...),
):
    # Aquí puedes guardar los datos editados en la base de datos o en sesión
    # Por ahora, solo regresamos los datos modificados
    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request,
            "name": name,
            "full_name": full_name,
            "address": address,
            "phone": phone,
            "email": email,
            "profile": profile,
            "work_experience": work_experience,
            "education": education,
            "skills": skills,
            "certifications": certifications,
            "languages": languages,
            "references": references,
            "dob": dob,
        }
    )

@app.post("/curriculum", response_class=HTMLResponse)
async def submit_curriculum(
    request: Request,
    name: str = Form(...),
    lang: str = Form(...),
    full_name: str = Form(...),
    address: str = Form(...),
    phone: str = Form(...),
    email: str = Form(...),
    dob: str = Form(...),
    photo: UploadFile = File(...),  # Agregar campo para la foto
    profile: str = Form(...),
    work_experience: str = Form(...),
    education: str = Form(...),
    skills: str = Form(...),
    certifications: str = Form(...),
    languages: str = Form(...),
    references: str = Form(...),
):
    photo_filename = save_photo(photo)  # Guardar la foto
    age = calculate_age(dob)  # Calcular la edad
    texts = load_texts(lang)
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "texts": texts,
            "lang": lang,
            "name": name,
            "full_name": full_name,
            "address": address,
            "phone": phone,
            "email": email,
            "dob": dob,
            "age": age,
            "photo_filename": photo_filename,  # Pasar el nombre del archivo de la foto
            "profile": profile,
            "work_experience": work_experience,
            "education": education,
            "skills": skills,
            "certifications": certifications,
            "languages": languages,
            "references": references,
        },
    )

# Proyecto Final de Almacenamiento de Datos

Este repositorio contiene el proyecto final del curso, desarrollado con **FastAPI**.  
La API permite gestionar y almacenar información relacionada con eventos y su contexto académico (programas, facultades, participantes, etc.), usando una arquitectura organizada por módulos.

## Tecnologías utilizadas

- **Python 3.10+**
- **FastAPI**
- **Uvicorn** 
- **SQLAlchemy** 
- Archivo `.env` para variables de entorno

## Requisitos previos

Antes de ejecutar el proyecto, asegúrate de tener instalado:

- [Python 3.10 o superior](https://www.python.org/downloads/)
- `pip` (gestor de paquetes de Python)
- Opcional pero recomendado: un entorno virtual (`venv`)

## Instalación

1. Clonar el repositorio:

   ```bash
   git clone https://github.com/Sxg0673/Proyecto_Final_Almacenamiento_Dato.git
   cd Proyecto_Final_Almacenamiento_Dato
   
2. (Opcional) Crear y activar un entorno virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate   # En macOS / Linux
   # .\venv\Scripts\activate  # En Windows
   
3. Instalar dependencias:
 ```bash
pip install -r requirements.txt
```

4. Ejecución del proyecto (desde la raíz del repositorio):
```bash
uvicorn app.main:app --reload

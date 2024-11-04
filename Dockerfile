# Usa una imagen oficial de Python como base
FROM python:3.11.0

# Establece el directorio de trabajo en el contenedor
WORKDIR /WORKDIR

# Copia los archivos del proyecto al contenedor
COPY . /WORKDIR

# Instala las dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Crea un entorno virtual en el contenedor y actívalo
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"  

# Actualiza pip a la última versión
RUN pip install --upgrade pip

# Instala las dependencias de Python listadas en requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto 8000 para que Railway pueda acceder
EXPOSE 8000

# Comando para iniciar el servidor (asegúrate de que apunte a la ubicación correcta)
CMD ["python", "orian_backend_django/manage.py", "runserver", "0.0.0.0:8000"]

# Usa una imagen oficial de Python como base
FROM python:3.11.0
# Establece el directorio de trabajo dentro del contenedor
WORKDIR /WORKDIR/orian_backend_django

# Copy the current directory contents into the container at /WORKDIR/orian_backend_django
COPY . /WORKDIR/orian_backend_django

# Instala las dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Crea un entorno virtual en el contenedor y actívalo
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"  

# Instala las dependencias de Python listadas en requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia todos los archivos de tu proyecto al directorio de trabajo en el contenedor
COPY . .

# Expone el puerto 8000 para que Railway pueda acceder
EXPOSE 8000

# Comando para iniciar el servidor (puedes modificarlo según tus necesidades)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

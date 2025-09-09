# Usa una imagen oficial de Python 3.11
FROM python:3.11-slim-buster

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de requirements primero (para cachear dependencias)
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código
COPY . .

# Comando para ejecutar el bot
CMD ["python", "bot.py"]

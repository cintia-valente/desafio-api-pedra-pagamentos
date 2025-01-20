# Use a imagem oficial do Python
FROM python:3

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia o arquivo requirements.txt para o diretório de trabalho
COPY src/requirements.txt /app/

# Instala as dependências do Python
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copia o restante do código da aplicação para dentro do contêiner
COPY . /app/

# Define a variável de ambiente para o Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Exponha a porta em que o Flask vai rodar
EXPOSE 5000

COPY scripts /scripts

# Comando para rodar a aplicação Flask
# Espera o banco de dados estar disponível e depois carrega o CSV

#CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
CMD ["sh", "-c", "python /scripts/load_data.py && gunicorn --reload -b 0.0.0.0:5000 app:app"]


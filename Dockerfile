# Usa uma imagem oficial do Python como base
FROM python:3.9

# Define o diretório de trabalho no contêiner
WORKDIR /app

# Copia os arquivos do projeto para dentro do contêiner
COPY . /app

# Instala as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Comando para rodar o bot
CMD ["python", "NbaCareerBot.py"]

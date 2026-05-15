# Usa uma imagem leve do python 3.11
FROM python:3.11-slim

# Diretório de trabalho dentro do container
WORKDIR /app

# Instala o Flask
RUN pip install --no-cache-dir Flask==3.0.3

# Copia todo o código para dentro do container
COPY . .

# Expõe a porta que a aplicação vai usar internamente
EXPOSE 6543

# Roda a aplicação quando o container iniciar
# O formato de array é usado pra pular o shell como intermeriário
CMD ["python", "backend/main.py"]
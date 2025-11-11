FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# O Render define a variável $PORT, então não precisamos expor manualmente
# EXPOSE 8000   <-- pode remover

CMD uvicorn ApiConsultaLivro:app --host 0.0.0.0 --port $PORT
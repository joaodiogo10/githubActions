FROM python:3.10

WORKDIR /usr/app
COPY ./requirements.txt .
ENV PYTHONPATH "${PYTHONPATH}:/usr/app/src"

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

EXPOSE 80
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]

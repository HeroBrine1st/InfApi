FROM python:3.8

ENV PIP_DISABLE_PIP_VERSION_CHECK 1

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY ./aerich.ini /aerich.ini
COPY ./src/ /src/

EXPOSE 80

CMD ["uvicorn", "inf:app", "--host", "0.0.0.0", "--port", "80", "--app-dir", "/src/"]

FROM 777555387664.dkr.ecr.us-east-1.amazonaws.com/oracle19.18-11g:latest

#RUN yum install -y oracle-epel-release-el7
RUN yum install -y python39
#RUN yum install -y python39 && \
#    python3 -m pip install oracledb==1.2.2 && poetry==1.2.0 \
#    rm -rf /var/cache/yum

ENV DB_USERNAME=sin_especificar
ENV DB_PASSWORD=sin_especificar
ENV DB_ENVIRONMENT=testing

COPY ./app /app
WORKDIR /app

RUN python3 -m pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Instalo Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/usr/local/poetry python3 - --version 1.4.2
ENV POETRY_HOME="/usr/local/poetry/bin"
ENV PATH="$PATH:$POETRY_HOME"

RUN #!/bin/sh \
    if [ -f "./app/pyproject.toml" ]; then \ 
      poetry install \ 
    else \
      echo "Poetry no se inicio en este proyecto" \
    fi

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]

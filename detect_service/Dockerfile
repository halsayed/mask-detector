FROM tensorflow/tensorflow

RUN apt-get update && apt-get install -y libglu1-mesa

COPY requirements.txt ./
RUN pip install -U pip && pip install -r requirements.txt

# application folder
RUN mkdir /app
WORKDIR /app

# python requirements
COPY . /app

# run mask detect service
CMD ["python","/app/background_service.py"]
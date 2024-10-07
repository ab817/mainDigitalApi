FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
ENV TZ=Asia/Kathmandu
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
EXPOSE 8000
CMD python manage.py runserver 0.0.0.0:8000
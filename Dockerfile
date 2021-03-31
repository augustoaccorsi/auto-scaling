FROM python:3

ENV AUTO_SCALING_GROUP=web-app-asg
ENV REGION=sa-east-1
ENV ENV=prod

ADD . /bat-files
ADD . /data-set
WORKDIR /app
COPY . /app

RUN pip install apscheduler
RUN pip install openpyxl
RUN pip install xlsxwriter
RUN pip install datetime
RUN pip install timedelta

ENTRYPOINT ["python"]
CMD ["run.py"]
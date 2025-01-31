FROM python:3

ENV AUTO_SCALING_GROUP=web-app-asg
ENV REGION=sa-east-1
ENV ENV=prod

ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG AWS_REGION=sa-east-1

RUN pip install apscheduler
RUN pip install openpyxl
RUN pip install xlsxwriter
RUN pip install datetime
RUN pip install timedelta
RUN pip install awscli
RUN pip install subprocess.run
RUN pip install boto3

WORKDIR /app/
COPY . /app/

EXPOSE 6000
CMD ["python", "run.py"]
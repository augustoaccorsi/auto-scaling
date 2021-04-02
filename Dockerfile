FROM python:3

ENV AUTO_SCALING_GROUP=web-app-asg
ENV REGION=sa-east-1
ENV ENV=prod
ENV ACCESS_KEY=ASIAYKIIUWQT5F4M5J6A
ENV SECRET_KEY=Reiu3ITS1w34lWQqoCnpmcdcPw+6vlUnFIC5m8Ix
ENV SESSION_TOKEN=IQoJb3JpZ2luX2VjEH0aCXNhLWVhc3QtMSJHMEUCIQCwDOj2jnmOWF1Kgj37iWPF/zYqJ9MyV3lI1oTrihG00AIgLqcO/sMcI9QOfFuwD9+2rGwb2cNQnJIV1fyKXRaULMEq3AEIxv//////////ARAAGgw1NzE3ODU2NTUzMzUiDDpa9BwRVvxzwdB9ISqwAQN5+sSuqCkwDo/EBUB6ogRE8lEnJ29vXqBVnX4ROtk41G9eoILIQuzkcrsFsyjxfgbHiueOeCV2cNDDZWfK45gQ9wdpgaVts64pbdW9sVRE+qjQCrhPbz1i/z9dcPO3DcKUYX/eoQidfJE8yFhRfhQmo2a0C98mwBPHwQXYD/Amr1eiRhDwFjfhcIOfJs9jkE+vUlDfX++MY7n1dtd16dJOh3THcQ2J0wiDrLkYfyoqMJuKnoMGOpgB7oYcUfol4UYHdVE3IZJgQzEqrrVIogLNuEF4Bp6509R0+pxU+/t7B4VOM3efMHMkVUs0XFQxjUOQdh0tlUyg2TLLb3THfFvtPGT7Nzs6g6uavMN4JWcGkpP8NpQT4+dT4vUGaauOyHTKCb27g5Craa/URmOwug9jSQQX1q4n2qrpbwujIMQRJrC6+a5wk7sK1Df2evCWTx8=


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
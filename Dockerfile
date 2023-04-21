FROM python:3.11.3-slim
WORKDIR /app
COPY . .
ENV TZ=Asia/Shanghai
RUN apt-get update \
  && apt-get -y install procps \
  && pip install -i https://mirrors.aliyun.com/pypi/simple --no-cache-dir -r production.txt \
  && chmod +x startup.sh
EXPOSE 80
VOLUME [ "/app/data" ]
ENTRYPOINT [ "./startup.sh" ]
CMD [ "-w", "4", "-l", "error" ]

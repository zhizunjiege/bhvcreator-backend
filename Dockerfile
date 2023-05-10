FROM node:18.16.0 AS frontend
WORKDIR /app
RUN git clone https://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@github.com/zhizunjiege/bhvcreator-frontend.git frontend \
  && cd frontend \
  && npm install \
  && npm run build

FROM python:3.11.3-slim
WORKDIR /app
COPY . .
COPY --from=frontend /app/frontend/dist /app/static
ENV TZ=Asia/Shanghai
RUN apt-get update \
  && apt-get -y install procps \
  && pip install -i https://mirrors.aliyun.com/pypi/simple --no-cache-dir -r production.txt \
  && chmod +x startup.sh
EXPOSE 80
VOLUME [ "/app/data" ]
ENTRYPOINT [ "./startup.sh" ]
CMD [ "-w", "4", "-l", "error" ]

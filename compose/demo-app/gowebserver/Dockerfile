FROM golang:alpine3.17 AS build
WORKDIR /go/src/app
COPY ./go/src/app/main.go .
RUN go build -o ./bin/webserver ./main.go

FROM alpine:3.17
ENV WORKSPACE=${WORKSPACE}
COPY --from=build /go/src/app/bin /go/bin
EXPOSE 8080
ENTRYPOINT /go/bin/webserver

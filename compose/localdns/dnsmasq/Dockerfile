FROM alpine:3.20

RUN apk --no-cache add dnsmasq

EXPOSE 53 53/udp

ENTRYPOINT ["dnsmasq"]
CMD ["--keep-in-foreground"]

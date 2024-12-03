FROM debian:bookworm-slim

ENV APT_CACHER_NG_VERSION=3.7.4

COPY entrypoint.sh /sbin/entrypoint.sh

RUN set -uex; \
    apt-get update -y; \
    DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -y \
      apt-cacher-ng=${APT_CACHER_NG_VERSION}* ca-certificates; \
    cp /etc/apt-cacher-ng/acng.conf /etc/apt-cacher-ng/acng.conf.original; \
    apt-get clean all; \
    rm -rf /var/lib/apt/lists/*; \
    chmod 755 /sbin/entrypoint.sh;

EXPOSE 3142/tcp

VOLUME ["/var/cache/apt-cacher-ng","/var/log/apt-cacher-ng"]

ENTRYPOINT ["/sbin/entrypoint.sh"]

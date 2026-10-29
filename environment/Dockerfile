FROM debian:bookworm-slim

# python for the verifier + a normal-looking user set
RUN apt-get update && apt-get install -y --no-install-recommends python3 \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd -g 1000 user && useradd -u 1000 -g 1000 -m -s /bin/bash user \
    && useradd -u 1200 -g 100 mediahouse-svc -m 2>/dev/null || true

WORKDIR /app

COPY workspace/rootfs/var /var/
COPY workspace/rootfs/etc /etc/
COPY workspace/rootfs/home /home/
COPY workspace/rootfs/usr /usr/
COPY workspace/rootfs/root /root/
COPY workspace/rootfs/app /app/
COPY workspace/rootfs/srv /srv/

RUN mkdir -p /logs/verifier /var/www/html/wp-content/uploads/media-tools \
    && chown -R root:root /usr/local/lib \
    && chmod 755 /usr/local/lib/.telemetry-agent \
    && chmod 600 /var/spool/cron/crontabs/root \
    && chmod 700 /home/user/.ssh \
    && chmod 600 /home/user/.ssh/authorized_keys

CMD ["/bin/bash"]

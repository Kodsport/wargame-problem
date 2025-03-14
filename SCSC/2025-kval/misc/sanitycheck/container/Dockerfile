FROM ubuntu:22.04 AS chroot

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y python3

RUN groupadd -g 1337 ctf && useradd -r -u 1337 -g ctf ctf
RUN mkdir -p /home/ctf/

COPY main.py /home/ctf/
COPY flag.txt /home/ctf/

FROM ghcr.io/google/nsjail/nsjail:latest

COPY --from=chroot / /chroot

ENTRYPOINT nsjail --port 1337 --chroot /chroot/ --user 1337 --group 1337 --cwd /home/ctf/ --tmpfsmount /tmp --bindmount_ro /etc/resolv.conf:/etc/resolv.conf /usr/bin/python3 /home/ctf/main.py

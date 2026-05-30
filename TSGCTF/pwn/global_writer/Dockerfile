FROM ubuntu@sha256:1c4cc37c10c4678fd5369d172a4e079af8a28a6e6f724647ccaa311b4801c3c9


RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get install -y \
    xinetd \
    iproute2

RUN groupadd -r user && useradd -r -g user user

COPY --chown=root:user ./build/start.sh /home/user/start.sh
COPY --chown=root:user ./build/flag.txt /home/user/flag.txt
COPY --chown=root:user ./chal /home/user/chal
COPY --chown=root:root ./build/ctf.conf /etc/xinetd.d/ctf

WORKDIR /home/user

RUN chmod 444 ./flag.txt && \
    chmod 555 ./chal && \
    chmod 555 ./start.sh && \
    chmod 444 /etc/xinetd.d/ctf

RUN mv ./flag.txt ./flag-$(md5sum flag.txt | awk '{print $1}').txt

USER user
EXPOSE 58554

CMD ["xinetd", "-dontfork", "-f","/etc/xinetd.d/ctf"]

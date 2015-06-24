FROM ubuntu:14.04

# Reduce warnings
ENV DEBIAN_FRONTEND noninteractive

# Install deps
RUN apt-get update && apt-get install -y \
    python python-pip && \
	pip install boto

# Install script
COPY ./dyn53.py /usr/bin/

# Start
ENTRYPOINT ["/usr/bin/dyn53.py"]

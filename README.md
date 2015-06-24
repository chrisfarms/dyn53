# dyn53

`dyn53` is a dynamic DNS update daemon, built to run in a docker container that periodically checks the machine's WAN IP address then updates a DNS record using Amazon's Route53.

It polls various free "what's my IP" type services to discover the IP address.

## Dependencies

* Docker

## Usage

Options are passed via environment variables. You will need to provide:

* `DYN53_DOMAIN` : The DNS record to update (ie. xxx.example.com)
* `AWS_ACCESS_KEY_ID` : Your Amazon key
* `AWS_SECRET_ACCESS_KEY` : Your Amazon secret.

Docker run example:

```
docker run --rm --name dyn53 \
	-e DYN53_DOMAIN=<YOUR_DOMAIN> \
	-e AWS_ACCESS_KEY_ID=<YOUR_KEY> \
	-e AWS_SECRET_ACCESS_KEY=<YOUR_SECRET> \
	chrisfarms/dyn53
```

## Example systemd unit

Since this would most commonly be run as a service, here's an example systemd unit.

```
[Unit]
Description=Dynamic DNS update service
After=docker.service

[Service]
ExecStartPre=-/usr/bin/docker rm -f dyn53
ExecStart=/usr/bin/docker run --rm -t \
	--name dyn53 \
	-e DYN53_DOMAIN=<YOUR_DOMAIN> \
	-e AWS_ACCESS_KEY_ID=<YOUR_KEY> \
	-e AWS_SECRET_ACCESS_KEY=<YOUR_SECRET> \
chrisfarms/dyn53
ExecStop=-/usr/bin/docker stop dyn53
TimeoutStartSec=0
KillMode=none
Restart=always
RestartSec=10s
StartLimitInterval=0
```

## Building

Use `make` to rebuild the container, and `make release` to update the image on docker hub.

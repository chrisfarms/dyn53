default: build

SHELL := /bin/bash
PWD := $(shell pwd)

build:
	docker build -t chrisfarms/dyn53 .

run: build
	docker run \
		-it --rm \
		--name dyn53 \
		-e DYN53_DOMAIN=$(DYN53_DOMAIN) \
		-e AWS_ACCESS_KEY_ID=$(AWS_ACCESS_KEY_ID) \
		-e AWS_SECRET_ACCESS_KEY=$(AWS_SECRET_ACCESS_KEY) \
		chrisfarms/dyn53

release: build
	docker push chrisfarms/dyn53

clean:
	docker rmi chrisfarms/dyn53 || echo 'ok'

.PHONY: default build run release clean enter

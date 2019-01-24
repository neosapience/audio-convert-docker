name := neosapience/audio-convert
tag := 0.0.6
pwd := $(shell pwd)

build:
	@docker build . -t ${name}:${tag} -t ${name}:latest

build-sub:
	@docker build . -f Dockerfile-build -t ${name}:${tag}-sub

test:
	@docker run --rm -it -v ${pwd}:/opt/audio-convert ${name}:${tag} pytest

ls:
	@docker images ${name}

run:
	@docker run --rm -it -P ${name}:${tag}

dev:
	@docker run --rm -it -v ${pwd}:/opt/audio-convert  ${name}:${tag} sh

push:
	@docker push ${name}:${tag}

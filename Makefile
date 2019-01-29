name := neosapience/audio-convert
tag := dev
pwd := $(shell pwd)

build:
	@docker build . -t ${name}:${tag}

build-sub:
	@docker build . -f Dockerfile-build -t ${name}:${tag}-sub

test:
	@docker run --rm -it -v ${pwd}:/opt/audio-convert ${name}:${tag} pytest -lvs

ls:
	@docker images ${name}

run:
	@docker run --rm -it -P ${name}:${tag}

dev:
	@docker run --rm -it -v ${pwd}:/opt/audio-convert  ${name}:${tag} sh

push:
	@docker push ${name}:${tag}

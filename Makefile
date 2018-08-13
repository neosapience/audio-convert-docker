name := neosapience/audio-convert
tag := 0.0.2
pwd := $(shell pwd)

build:
	@docker build . -t ${name}:${tag} -t ${name}:latest

ls:
	@docker images ${name}

run:
	@docker run --rm -it -P ${name}:${tag}

dev:
	@docker run --rm -it -v ${pwd}:/opt/audio-convert  ${name}:${tag} sh

push:
	@docker push ${name}:${tag}

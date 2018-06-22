name := neosapience/audio-convert
tag := 0.0.1
pwd := $(shell pwd)

build:
	@docker build . -t ${name}:${tag} -t ${name}:latest

ls:
	@docker images ${name}

run:
	@docker run --rm -it -p 5000:5000 ${name}:${tag}

dev:
	@docker run --rm -it -v $(pwd):/code  ${name}:${tag} sh

push:
	@docker push ${name}:${tag}

name := neosapience/audio-convert
tag := 0.0.1

build:
	@docker build . -t ${name}:${tag} -t ${name}:latest

ls:
	@docker images ${name}

run:
	@docker run --rm -it -p 5000:5000 ${name}:${tag}

push:
	@docker push ${name}:${tag}

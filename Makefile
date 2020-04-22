TAG=${GITHUB_REF}

.PHONY: all test generate build package clean

all: deps

pytest:
	pytest --cov=./ --cov-report=xml

pylint:
	pytest --pylint

test: pytest pylint

deps:
	python3 -m pip install -v -r requirements.txt

tag_no_slash := $(subst /,-,${TAG})

docker:
	docker build -t docker.pkg.github.com/bangersnmash/smg/smg_server:local .

docker-ci:
	docker build -t docker.pkg.github.com/bangersnmash/smg/smg_server:${tag_no_slash} .

docker-push:
	docker push docker.pkg.github.com/bangersnmash/smg/smg_server:${tag_no_slash}

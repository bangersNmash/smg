TAG?=0.0.1

.PHONY: all test generate build package clean

all: deps

pytest:
	pytest --cov=./ --cov-report=xml

pylint:
	pytest --pylint

test: pytest pylint

deps:
	python3 -m pip install -v -r requirements.txt

docker:
	docker build -t docker.pkg.github.com/bangersnmash/smg/smg_server:local .

docker-ci:
	docker build -t docker.pkg.github.com/bangersnmash/smg/smg_server:${GITHUB_REF} .



.PHONY: run
run:
	echo TODO

.PHONY: lint
lint:
	yarn tsc
	mypy server/


.PHONY: server
server:
	python server/app.py

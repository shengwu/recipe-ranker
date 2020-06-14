
.PHONY: run
run:
	echo TODO

.PHONY: python-check-types
python-check-types:
	mypy server/


.PHONY: server
server:
	python server/app.py

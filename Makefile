DIST?=dist/

default: dist

.PHONY: dist
dist:
	mkdir -p $(DIST)
	python3 -m pep517.build -o $(DIST) .
	dir2pi $(DIST)

install:
	python3 -m pip install --upgrade --force .

setup:
	python3 -m pip install --upgrade pip
	python3 -m pip install pep517 setuptools pip2pi


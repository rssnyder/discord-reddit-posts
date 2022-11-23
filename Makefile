.POSIX:
.SUFFIXES:

.PHONY: default
default: dist

venv:
	python3 -m venv venv
	./venv/bin/python3 -m pip install -r requirements.txt

.PHONY: build
build: 
	rm -fr build/
	python3 -m pip install -q -r requirements.txt --target build/
	rm -fr build/*.dist-info/
	cp main.py build/__main__.py
	python3 -m zipapp -c -p "/usr/bin/env python3" -o discord-reddit-posts build/

.PHONY: dist
dist: build
	rm -fr dist/
	mkdir dist/
	cp discord-reddit-posts dist/

.PHONY: package
package: dist
	nfpm package -p deb -t discord-reddit-posts.deb

.PHONY: clean
clean:
	rm -fr discord-reddit-posts *.deb dist/ build/
test:
	pytest-3 -v

lint:
	python3 -m flake8 dotgit --count --statistics --show-source

package:
	python3 setup.py sdist bdist_wheel

clean:
	rm -rf build dist dotgit.egg-info

test:
	pytest-3

package:
	python3 setup.py sdist bdist_wheel

clean:
	rm -rf build dist dotgit.egg-info

run:
	PYTHONPATH=. python3 bin/dotgit -h

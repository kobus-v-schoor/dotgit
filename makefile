test:
	tests/test.py -v

package:
	python3 setup.py sdist bdist_wheel

clean:
	rm -rf build dist dotgit.egg-info

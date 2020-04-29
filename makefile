test:
	tests/test.py -v

package:
	python3 setup.py sdist bdist_wheel

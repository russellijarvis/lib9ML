
.PHONY: doc test


doc:
	make -C ./doc/python_nineml_api/ html

test:
	make -C ./test


clean:
	make -C ./doc clean
	make -C ./test clean


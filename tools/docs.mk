$(eval sphinx       := $(venvpath)/bin/sphinx-build)

setup-docs: setup-virtualenv3
	@$(pip3) --quiet install --requirement requirements-docs.txt

## Build the documentation
docs-html: setup-docs
	touch doc/source/index.rst
	export SPHINXBUILD="`pwd`/$(sphinx)"; cd doc; make html

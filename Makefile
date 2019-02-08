.PHONY: init doc fmt
MAKEFILE_DIR = $(abspath $(patsubst %/,%,$(dir $(abspath $(lastword $(MAKEFILE_LIST))))))

init:
	wget https://chromedriver.storage.googleapis.com/$$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_mac64.zip --delete-after -O /tmp/chromedriver
	unzip /tmp/chromedriver

doc:
	pyreverse -o png $$(find "${MAKEFILE_DIR}" -type f -name '*.py' -print)

fmt:
	${MAKEFILE_DIR}/pyfmt.sh -f ${MAKEFILE_DIR}



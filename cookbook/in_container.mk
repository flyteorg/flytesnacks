.PHONY: clean
clean:
	rm -rf /tmp/flyte

/tmp/flyte/_pb_output: clean
	mkdir -p /tmp/flyte/_pb_output

.PHONY: register
register: serialize
	flyte-cli register-files -h ${FLYTE_HOST} ${INSECURE_FLAG} -p ${PROJECT} -d development -v ${VERSION} /tmp/flyte/_pb_output/*

.PHONY: serialize
serialize: /tmp/flyte/_pb_output
	pyflyte --config /root/sandbox.config serialize workflows -f /tmp/flyte/_pb_output

.PHONY: fast_serialize
fast_serialize: /tmp/flyte/_pb_output
	pyflyte --config /root/sandbox.config serialize fast workflows -f /tmp/flyte/_pb_output

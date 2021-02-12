.PHONY: serialize
serialize:
	pyflyte --config /root/sandbox.config serialize workflows -f /tmp/output

.PHONY: fast_serialize
fast_serialize:
	pyflyte --config /root/sandbox.config serialize fast workflows -f /tmp/output

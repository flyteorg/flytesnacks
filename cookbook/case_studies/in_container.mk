.PHONY: serialize_sandbox
serialize_sandbox:
	pyflyte --config /root/sandbox.config serialize workflows -f /tmp/output

.PHONY: fast_serialize_sandbox
fast_serialize_sandbox:
	pyflyte --config /root/sandbox.config serialize fast workflows -f /tmp/output

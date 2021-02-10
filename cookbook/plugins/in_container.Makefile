.PHONY: serialize_sandbox
serialize_sandbox:
	pyflyte --config /root/sandbox.config serialize workflows -f /tmp/output

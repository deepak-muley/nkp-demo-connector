.PHONY: build push package chart-version

VERSION ?= 1.0.0
IMAGE ?= ghcr.io/deepak-muley/demo-connector
CHART_REGISTRY ?= oci://ghcr.io/deepak-muley/charts

# Build the container image
build:
	docker build -t $(IMAGE):$(VERSION) .
	docker tag $(IMAGE):$(VERSION) $(IMAGE):latest

# Push the container image (requires docker login)
push: build
	docker push $(IMAGE):$(VERSION)
	docker push $(IMAGE):latest

# Package the Helm chart
package:
	helm package chart/ --version $(VERSION)

# Push the Helm chart to OCI (requires helm registry login)
chart-push: package
	helm push demo-connector-$(VERSION).tgz $(CHART_REGISTRY)
	rm -f demo-connector-$(VERSION).tgz

# Full release: build image, push image, package chart, push chart
release: push chart-push

# NKP Demo Connector

A **sample application** for demonstrating NKP AI catalog composability. It depends on [Weaviate](https://www.weaviate.io/) and verifies connectivity by displaying a simple status page.

## Purpose

This app showcases:

- **Catalog dependency flow** — Enable Weaviate in the workspace first, then enable this app
- **In-cluster discovery** — Connects to Weaviate via Kubernetes DNS
- **Zero-config** — Uses default Weaviate URL; works when both are in the same workspace

## Prerequisites

- **Weaviate** must be enabled in the same NKP workspace before enabling this app
- Deploy from the [NKP AI Applications Catalog](https://github.com/nutanix-cloud-native/nkp-ai-applications-catalog)

## Usage

1. Enable **Weaviate** from the NKP UI
2. Wait for Weaviate to be ready
3. Enable **Demo Connector** from the NKP UI
4. Open the app URL (LoadBalancer or via Launch button)
5. You should see "Weaviate: Connected"

## Configuration

| Environment Variable | Default | Description |
|----------------------|---------|-------------|
| `WEAVIATE_URL` | `http://weaviate.weaviate.svc.cluster.local:80` | Weaviate REST API URL |

Override via Helm values if your Weaviate instance uses a different namespace or release name.

## Development

### Build and run locally

```bash
# Install dependencies
pip install -r src/requirements.txt

# Set Weaviate URL (or use default)
export WEAVIATE_URL=http://localhost:8080  # or your Weaviate URL

# Run
python src/app.py
```

### Build container and Helm chart

```bash
# Build image
make build

# Push image and chart (requires docker/helm login)
make release VERSION=1.0.0
```

### Release (GitHub Actions)

Push a version tag to trigger a release:

```bash
git tag v1.0.0
git push origin v1.0.0
```

This builds the image, pushes to `ghcr.io/deepak-muley/demo-connector`, and pushes the Helm chart to `oci://ghcr.io/deepak-muley/charts`.

## Catalog Entry

This app is registered in the NKP AI Applications Catalog as `demo-connector`:

- **Catalog path:** `applications/demo-connector/1.0.0/`
- **Source:** [github.com/deepak-muley/nkp-demo-connector](https://github.com/deepak-muley/nkp-demo-connector)

## License

MIT

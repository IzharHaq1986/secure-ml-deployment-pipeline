## CI / Security Status

![Docker Smoke Test](<badge-markdown-from-github>)
![Trivy Container Scan](<badge-markdown-from-github>)
![Generate SBOM](<badge-markdown-from-github>)
![Cosign Sign Image](<badge-markdown-from-github>)
![Cosign Verify Image](<badge-markdown-from-github>)

## Verifiable Deployment Path

This repository demonstrates a security-focused ML deployment path:

- Model service build
- Container smoke validation
- Vulnerability scanning
- SBOM generation
- Container image signing
- Signature verification

## Security Artifacts

The pipeline produces and validates these controls:

- Container runtime validation through GitHub Actions
- Trivy-based vulnerability scanning
- SPDX SBOM generation
- Cosign keyless signing
- Cosign verification against the published GHCR image

## Verify the Published Image

Example verification flow:

```bash
IMAGE_URI=ghcr.io/<owner>/<repo>@sha256:<digest>

cosign verify \
  --certificate-identity "https://github.com/<owner>/<repo>/.github/workflows/cosign-sign.yml@refs/heads/main" \
  --certificate-oidc-issuer "https://token.actions.githubusercontent.com" \
  "$IMAGE_URI"

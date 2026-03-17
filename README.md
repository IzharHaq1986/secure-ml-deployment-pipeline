## CI / Security Status

![Docker Smoke Test](https://github.com/IzharHaq1986/secure-ml-deployment-pipeline/actions/workflows/docker-smoke.yml/badge.svg)

![Trivy Container Scan](https://github.com/IzharHaq1986/secure-ml-deployment-pipeline/actions/workflows/trivy-scan.yml/badge.svg)

![Generate SBOM](https://github.com/IzharHaq1986/secure-ml-deployment-pipeline/actions/workflows/sbom.yml/badge.svg)

![Cosign Sign Image](https://github.com/IzharHaq1986/secure-ml-deployment-pipeline/actions/workflows/cosign-sign.yml/badge.svg)

![Cosign Verify Image](https://github.com/IzharHaq1986/secure-ml-deployment-pipeline/actions/workflows/cosign-verify.yml/badge.svg)

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

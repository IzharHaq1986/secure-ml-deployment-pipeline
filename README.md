## CI / Security Status

## Tech Stack

![Python](https://img.shields.io/badge/Python-3.12-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-0.129-green) ![Docker](https://img.shields.io/badge/Docker-Container-blue) ![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-CI/CD-black) ![Trivy](https://img.shields.io/badge/Security-Trivy-red) ![Cosign](https://img.shields.io/badge/SupplyChain-Cosign-purple) ![SBOM](https://img.shields.io/badge/SBOM-SPDX-orange)

---

## Verifiable Deployment Path

This repository demonstrates a security-focused ML deployment path:

- Model service build
- Container smoke validation
- Vulnerability scanning
- SBOM generation
- Container image signing
- Signature verification

---

## Security Artifacts

The pipeline produces and validates these controls:

- Container runtime validation through GitHub Actions
- Trivy-based vulnerability scanning
- SPDX SBOM generation
- Cosign keyless signing
- Cosign verification against the published GHCR image

---

## Environment-Based Deployment

The deployment layer supports environment-based configuration through Docker Compose.

### 1. Create a local environment file

Copy the example file:

```bash
cp .env.example .env
```
---

## Verify the Published Image

Example verification flow:

```bash
IMAGE_URI=ghcr.io/<owner>/<repo>@sha256:<digest>

cosign verify \
  --certificate-identity "https://github.com/<owner>/<repo>/.github/workflows/cosign-sign.yml@refs/heads/main" \
  --certificate-oidc-issuer "https://token.actions.githubusercontent.com" \
  "$IMAGE_URI"
```

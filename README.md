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

---

## Agent Security Enforcement

The project includes a lightweight policy enforcement layer for untrusted
agent-triggered actions.

## Security Controls Implemented

- centralized policy engine for action enforcement
- default-deny behavior for unregistered actions
- validated external input boundary for agent-submitted requests
- explicit separation between external request models and internal enforcement models
- controlled HTTP 403 responses for policy violations
- audit logging for policy approvals and denials
- high-risk deployment gating with explicit approval checks

## Enforcement Flow

The current enforcement flow is:

Agent request -> validated API input -> internal action model -> policy engine -> allow/deny decision

## Example Protected Actions

Implemented examples include:

- `read_status`
  - low-risk read action
  - allowed only from approved sources

- `deploy_model`
  - high-risk deployment action
  - requires:
    - `source="agent"`
    - `risk_level="high"`
    - `parameters.approved=true`

## Auditability

Policy decisions are logged at runtime.

Examples:

- approved actions are logged at `INFO`
- denied actions are logged at `WARNING`

This provides a minimal audit trail for policy outcomes during local runs,
testing, and future deployment integration.

## Test Coverage

Policy enforcement behavior is covered by automated tests, including:

- public health endpoint
- protected health endpoint
- denied policy path
- validated low-risk action approval
- denied unapproved deployment
- approved high-risk deployment

## 1. Create a local environment file

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

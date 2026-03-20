# project_state.md

## Project
Secure ML Deployment Pipeline

## I. Project Overview

Secure ML Deployment Pipeline is a security-focused machine learning deployment demonstration project.

The project demonstrates a verifiable delivery path:

Model training → container build → validation → vulnerability scanning → SBOM → image signing → verification → deployment

## II. v1 Scope

Version 1 focuses on:

- minimal FastAPI inference service
- containerized deployment
- reproducible build process
- container security baseline
- CI/CD pipeline using GitHub Actions
- vulnerability scanning (Trivy)
- SBOM generation (SPDX via Syft)
- Cosign image signing (keyless)
- Cosign image verification
- documentation and architecture assets

## III. Implemented Pipeline Stages

1. Container build
2. Runtime validation (Docker smoke test)
3. Vulnerability scanning (Trivy)
4. SBOM generation
5. Image signing (Cosign)
6. Image verification (Cosign)

## IV. Current Status

The project is now:

- fully reproducible
- security-gated
- supply-chain verifiable
- deployment-capable
- CI/CD enforced
- deployment-enforced
- portfolio-ready

All pipeline stages are implemented, validated, and enforced in branch protection.

---

## V. Recently Completed

- Fixed Deploy Smoke workflow trigger so required deployment validation runs on all pull requests
- Added `.env.example` for portable Docker Compose runtime configuration
- Updated `docker-compose.yml` to use environment-variable interpolation for:
  - host port
  - CPU limits
  - memory limits
- Updated `.gitignore` to exclude local `.env` files
- Validated `.env`-driven Docker Compose deployment locally:
  - config validation
  - container startup
  - health endpoint check
  - clean teardown
- Added `.env.ci.example` for CI-specific Docker Compose runtime settings
- Updated `deploy-smoke.yml` to use the dedicated CI environment template
- Merged CI configuration refinement into `main`

---

## VI. Next Milestone

- Introduce policy-based controls for untrusted AI agent interaction
- Define least-privilege boundaries for deployment and verification actions
- Separate trusted deployment logic from untrusted agent-driven inputs
- Prepare a security-focused design note for agent-safe operations

---

## VII. Next Step

Create a security design note for untrusted AI agent integration.

Focus:

- external policy-based authorization
- least-privilege scoped credentials
- validated tool calls and sanitized inputs
- strict separation of trusted and untrusted context
- gated high-risk actions
- isolated identities, monitored runtime behavior, and constrained memory

---

## VIII. Phase Progress

Phase 1 — Engineering Implementation

- Repository setup → Completed
- Service implementation → Completed
- Containerization → Completed
- CI pipeline → Completed
- Vulnerability scanning → Completed
- SBOM generation → Completed
- Image signing → Completed
- Image verification → Completed
- Deployment stage (Docker Compose) → Completed
- Deployment validation (CI + local) → Completed
- Environment-based configuration → Completed
- CI-specific deployment configuration → Completed

Phase 2 — Production Readiness (In Progress)

- Security design for untrusted AI agents → Next
- Configuration strategy refinement → In Progress
- Kubernetes deployment → Planned





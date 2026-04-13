# Architecture of a Secure ML Deployment Pipeline

Most machine learning projects focus on model performance.

Far fewer focus on how the model is built, validated, and delivered in a way that can be trusted.

This project was designed to make the delivery path explicit and verifiable.

---

## I. Design Goal

The goal was not to build a complex system.

The goal was to make each stage of the pipeline answer a specific question:

- Was the container built correctly?
- Does it run as expected?
- Are there known vulnerabilities?
- What dependencies are included?
- Who produced the artifact?
- Is the deployment behaving correctly?

Each stage exists to produce a clear and testable outcome.

---

## II. End-to-End Flow

The pipeline follows a structured sequence:

1. Build container image  
2. Run container smoke test  
3. Scan for vulnerabilities (Trivy)  
4. Generate SBOM (Syft, SPDX)  
5. Sign image (Cosign, OIDC)  
6. Verify signature  
7. Deploy and validate  
8. Apply runtime policy checks  

Each stage produces an output that feeds into the next stage.

The pipeline is intentionally linear to keep behavior predictable and easy to debug.

---

## III. Trust Model

Trust is established through multiple independent layers:

- SBOM provides visibility into included dependencies  
- vulnerability scanning identifies known risks  
- image signing ensures artifact integrity  
- OIDC-based verification links artifacts to CI identity  

Instead of relying on static credentials, trust is tied to the build process and its origin.

This allows artifacts to be traced back to a specific repository and workflow.

---

## IV. Service Layer

The application layer is intentionally minimal.

Endpoints include:

- `/health`
- `/secure-health`
- `/agent/actions/validate`

The focus is not on feature richness, but on controlled behavior.

Requests entering the system are validated before being processed further.

---

## V. Policy Enforcement Layer

A lightweight policy engine sits between incoming requests and internal actions.

Responsibilities:

- evaluate incoming requests
- classify actions based on risk level
- allow or deny execution based on predefined rules

Examples:

- low-risk actions can proceed under defined conditions  
- high-risk actions require explicit approval  

This separation ensures that external input does not directly trigger internal operations.

---

## VI. Configuration Strategy

Configuration is treated as a controlled input.

Key properties:

- environment-backed values  
- strict validation at startup  
- no silent fallback behavior  

If required configuration is missing or invalid:

- the service does not start  

This keeps runtime behavior consistent across:

- local environments  
- CI pipelines  
- container deployments  

---

## VII. Deployment Baseline

Two deployment paths are supported:

### Docker Compose

- used for local validation and CI smoke testing  
- ensures the container can start and respond correctly  

### Kubernetes (Baseline)

- Deployment and Service manifests provided under `k8s/`  
- includes:
  - readiness and liveness probes  
  - resource constraints  
  - container security context  

The Kubernetes layer is intentionally minimal and designed to be extended.

---

## VIII. CI/CD as Integration Layer

GitHub Actions connects all stages of the pipeline.

Each workflow step validates one part of the system:

- container execution  
- vulnerability scanning  
- SBOM generation  
- signature verification  
- deployment response  

The pipeline acts as the integration point where all controls are exercised together.

---

## IX. What This Demonstrates

This project shows how commonly used tools can be combined into a coherent system.

It demonstrates:

- how artifacts move through a controlled pipeline  
- how multiple validation layers interact  
- how deployment behavior can be verified before runtime  

The emphasis is on clarity rather than complexity.

---

## X. Closing Thought

A deployment pipeline is not just a delivery mechanism.

It is a system for validating and tracing how artifacts move from source to runtime.

This project demonstrates how multiple independent controls can be composed into a single, verifiable delivery system.

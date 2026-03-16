# project_state.md

## Project
Secure ML Deployment Pipeline

## I. Project Overview

Secure ML Deployment Pipeline is a security-focused machine learning deployment demonstration project.

The project is intended to show how an ML model can move through a verifiable delivery path:

Model training → container build → image signing → SBOM → deployment

## II. v1 Scope

Version 1 will focus on:

- one small inference API
- one packaged model artifact
- Dockerized deployment
- GitHub Actions workflow foundation
- Cosign image signing
- SBOM generation
- simple deployment workflow
- documentation and architecture assets

## III. Planned Pipeline Stages

1. Model training
2. Container build
3. Image signing
4. SBOM generation
5. Deployment

## IV. Security Objectives

- establish artifact integrity
- support container provenance validation
- demonstrate signed image workflows
- provide dependency transparency through SBOM
- document a verifiable ML deployment path

## V. Current Repository State

Completed:

- GitHub repository created
- local repository initialized
- SSH authentication configured
- remote push successful
- initial directory structure created
- baseline documentation files added

## VI. Current Status

Project foundation established.

## VII. Next Step

Implement the minimal FastAPI service foundation for the ML inference pipeline.

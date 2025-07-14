# k8s demonstration

![k8s logo](./assets/k8s_logo.svg){ width="100" }

This repo demonstrates using Kubernetes (k8s) for some simple use cases.
The main purpose, is to see how viable it is as an alternative for small scale projects.

## Goals

- [ ] Terraform setup for AKS (Azure Kubernetes Service) k8s cluster
- [ ] ArgoCD setup for CI/CD
- [ ] Separate environments for dev, staging, and production
- [ ] Job with on-demand GPU node

## Getting started

To get started, set up the cluster

```bash
cd terraform
terraform init
terraform apply
```

Then set up the ArgoCD

```bash
cd argocd
kubectl apply -f argo-cd.yaml
```

And ...
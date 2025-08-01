# k8s demonstration

![k8s logo](./assets/k8s_logo.svg){ width="100" }

This repo demonstrates using Kubernetes (k8s) for some simple use cases.
The main purpose, is to see how viable it is as an alternative for small scale projects.

## Goals

Initial setup:

- [x] Terraform setup for AKS (Azure Kubernetes Service) k8s cluster
- [x] ArgoCD setup
- [x] Argo Workflows managed by ArgoCD
- [ ] Pass large data to inference job
- [x] Return large data from inference job

Long term:

- [ ] Separate environments for dev, staging, and production
- [ ] Job with on-demand GPU node

## Getting started

To get started, set up the cluster, navigate to the `infrastructure/terraform` directory, and run the following commands:

```bash
terraform init
terraform apply
```

Then, to get CLI access, run: `az aks get-credentials --resource-group k8s-demo-application --name aks-cluster`.
See the [Azure documentation](https://learn.microsoft.com/en-us/azure/aks/learn/quick-kubernetes-deploy-cli) for more details.

!!! tip

    Run `source <(kubectl completion zsh)` to enable command completion for `kubectl` in your terminal.

Then set up the ArgoCD (see more details in [the official documentation](https://argo-cd.readthedocs.io/en/stable/getting_started/)):

```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Expose the ArgoCD API server
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

and navigate to `https://localhost:8080` in your browser.

!!! tip "Notice the explicit `https` protocol"

!!! note "Getting credentials"

    ```bash
    argocd admin initial-password -n argocd
    argocd login <ARGOCD_SERVER>  # localhost:8080 if port-forwarded as above
    argocd account update-password
    ```

And we can now finally deploy the demo application:

```bash
kubectl apply -f k8s/demo/application.yaml
```

We'll now set up Argo Workflows:

```bash
kubectl apply -f k8s/argo-workflows/application.yaml -n argocd
```



## Good resources

- https://github.com/argoproj/argocd-example-apps/tree/master
- https://github.com/argoproj/argoproj-deployments/tree/master
- https://github.com/markti/terraform-hashitalks-2024/tree/main
- https://medium.com/@michael.cook.talk/argo-workflows-minio-nginx-8911b988b5c8
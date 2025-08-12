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

### Set up AKS

To get started, set up the cluster, navigate to the `infrastructure/terraform` directory, and run the following commands:

```bash
terraform init
terraform apply
```

Then, to get CLI access, run: `az aks get-credentials --resource-group k8s-demo-application --name aks-cluster`.
See the [Azure documentation](https://learn.microsoft.com/en-us/azure/aks/learn/quick-kubernetes-deploy-cli) for more details.

!!! tip

    Run `source <(kubectl completion zsh)` to enable command completion for `kubectl` in your terminal.


### Set up platform / helpers

#### Ingress Nginx

Navigate to `k8s/ingress-nginx`
```sh
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
helm install ingress-nginx ingress-nginx/ingress-nginx \
    --namespace ingress-nginx --create-namespace -f values.yaml
```

##### Set up cert manager

Install cert manager
```sh
helm install \
  cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  --set crds.enabled=true
```
and create cluster issuers

```sh
kubectl apply -f production-issuer.yaml -f staging-issuer.yaml
```

#### ArgoCD

Then set up the ArgoCD (see more details in [the official documentation](https://argo-cd.readthedocs.io/en/stable/getting_started/))

```sh
IP=$(kubectl -n ingress-nginx get svc ingress-nginx-controller \
     -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
DOMAIN="argocd.${IP}.sslip.io"
GRPC_DOMAIN="grpc.${DOMAIN}"

helm upgrade --install argo argo/argo-cd \
  -n argocd --create-namespace \
  -f values.yaml \
  --set-string global.domain="$DOMAIN" \
  --set-string "server.ingress.hosts[0]=$DOMAIN" \
  --set-string "server.ingressGrpc.hosts[0]=$GRPC_DOMAIN"
```


!!! note "Getting credentials"

    ```bash
    argocd admin initial-password -n argocd
    argocd login <ARGOCD_SERVER>  # grpc.argocd.{IP}.sslip.io if set up as above
    argocd account update-password
    ```

#### Argo Workflows

We'll now set up Argo Workflows:

```bash
kubectl apply -f k8s/argo-workflows/application.yaml -n argocd
```

### The Demo application

And we can now finally deploy the demo application:

```bash
kubectl apply -f k8s/demo/application.yaml
```




## Good resources

- https://github.com/argoproj/argocd-example-apps/tree/master
- https://github.com/argoproj/argoproj-deployments/tree/master
- https://github.com/markti/terraform-hashitalks-2024/tree/main
- https://medium.com/@michael.cook.talk/argo-workflows-minio-nginx-8911b988b5c8

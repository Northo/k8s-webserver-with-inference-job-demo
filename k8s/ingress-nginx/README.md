# Ingress-Nginx ingress controller setup

install helm and also cert-manager

```bash
helm install \
  cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  --set crds.enabled=true
```



# Ingress-Nginx ingress controller setup

## Set up Ingress-Nginx

```sh
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
helm install ingress-nginx ingress-nginx/ingress-nginx --namespace ingress-nginx --create-namespace -f values.yaml
```

## Set up cert manager

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

Now create ingresses with the [appropriate annotation](https://kubernetes.github.io/ingress-nginx/user-guide/tls/#automated-certificate-management-with-cert-manager) to make it use HTTPS.
For example 
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ingress-demo
  annotations:
    cert-manager.io/issuer: "letsencrypt-staging" # Replace this with a production issuer once you've tested it
    [..]
spec:
  tls:
    - hosts:
        - ingress-demo.example.com
      secretName: ingress-demo-tls
    [...]
```

See the Argo workflows, demo app, or kubernetes dashboard ingresses for real examples.


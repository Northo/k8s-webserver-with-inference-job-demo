# Lessons learned / Challanges

## Setting up Ingress controller

The Azure stuff was very confusing.
Tried using Nginx Ingress Controller, which was supposed to be simpler, but had some issues.
As written in <https://kubernetes.github.io/ingress-nginx/deploy/#quick-start>, there might be issues with managed providers.
So the recommendation is to run the cloud deploy manifest.

https://cert-manager.io/docs/releases/release-notes/release-notes-1.18/
```
  config:
    # Disable strict path validation, to work around a bug in ingress-nginx
    # https://github.com/kubernetes/ingress-nginx/issues/11176
    strict-validate-path-type: false
```

### Nginx-Ingress vs Ingress-Nginx
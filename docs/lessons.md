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

## Using manged identities

!!! info TODO

While using manged identities on AKS is in theory simple, I had some issues making it work.
The documentation from Azure was somewhat confusing, and did not suggest good ways to _test_ if it worked...

Two things must be in place from the cluster side (in addition to setting federation up in Azure)

1. The service account must have the correct client-id as an annotation
2. The pod must have the label `azure.workload.identity/use=true`

Sometimes, even with this, things seemed to now work.
I have not investigated thoroughly, but suspect either I set something wrong, or the order matters (like having the pod label during creating, not adding it after).



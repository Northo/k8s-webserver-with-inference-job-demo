# Lessons learned / Challanges

## Setting up Ingress controller

The Azure stuff was very confusing.
Tried using Nginx Ingress Controller, which was supposed to be simpler, but had some issues.
As written in <https://kubernetes.github.io/ingress-nginx/deploy/#quick-start>, there might be issues with managed providers.
So the recommendation is to run the cloud deploy manifest.
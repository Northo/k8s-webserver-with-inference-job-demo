# Platform

One of the big advantages of Kubernetes, is the rich ecosystem of tools and services that can be deployed on and integrated with it.
For this app, we leverage two tools from the [Argo project](https://argoproj.github.io/): [ArgoCD](https://argo-cd.readthedocs.io/en/stable/) for continuous deployment, and [Argo Workflows](https://argoproj.github.io/argo-workflows/) for managing the job execution.

## ArgoCD

![ArgoCD screenshot](https://argo-cd.readthedocs.io/en/stable/assets/argocd-ui.gif)

ArgoCD is a tool for continuous deployment in Kubernetes.
Whenever you push changes to a Git repository, ArgoCD will automatically deploy the changes to your Kubernetes cluster.
It also has a web UI;
the UI allows you to see the state of your application, and is a nice way to build some intuition with Kubernetes objects.

## Argo Workflows

![Argo Workflows screenshot](https://argo-workflows.readthedocs.io/en/stable/assets/screenshot.png)

While it is possible to run jobs directly in Kubernetes, we use Argo Workflows to manage the job execution.
Argo Workflows offer more flexible and advanced handling of jobs, such as retries, dependencies, and artifact management.


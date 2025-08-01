# Working with Kubernetes

While we recommend reading the [official Kubernetes documentation](https://kubernetes.io/docs/tutorials/kubernetes-basics/), we here give a brief overview of how to work with Kubernetes.

## Fundamental CLI

!!! tip

    The `kubectl` command provides very good command line completions.
    You can enable them by running:
    ```sh
    source <(kubectl completion YOUR_SHELL)
    ```
    where `YOUR_SHELL` is `bash`, `zsh`, `fish`, etc.

`kubectl` is the command line tool for interacting with Kubernetes.
It has a consistent syntax which lets you create, update, delete, and inspect various Kubernetes objects.
For example, to create a deployment, you can use:

!!! note "See [this section of the docs](https://kubernetes.io/docs/tutorials/kubernetes-basics/) for more details about the below examples."

```sh
# Create a deployment named "kubernetes-bootcamp" using the specified image
kubectl create deployment kubernetes-bootcamp --image=gcr.io/google-samples/kubernetes-bootcamp:v1

# Get a list of all deployments
kubectl get deployments

# Get detailed information about all pods
kubectl describe pods

# Expose the deployment as a service, making it accessible from outside the cluster
kubectl expose deployment/kubernetes-bootcamp --type="NodePort" --port 8080

# Delete the deployment and service
kubectl delete deployments/kubernetes-bootcamp services/kubernetes-bootcamp
```

## Working with YAML


Normally, we do not use `kubectl` to create objects directly.
Instead, we define our objects in YAML files, and then use `kubectl apply` to create or update them.
This allows us to version control our Kubernetes configuration, and makes it easier to manage complex applications.

!!! note "See [this section of the docs](https://kubernetes.io/docs/tasks/run-application/run-stateless-application-deployment/) for more details about the below examples."

```yaml
# nginx-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  selector:
    matchLabels:
      app: nginx
  replicas: 2 # tells deployment to run 2 pods matching the template
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.14.2
        ports:
        - containerPort: 80
```

## Helm and Kustomize

You'll probably come over [Helm](https://helm.sh/) and [Kustomize](https://kustomize.io/) in your Kubernetes journey.
While they are slightly more advanced topics, they are often super helpful, and worth mentioning here.

Helm is a package manager for Kubernetes, which allows you to define, install, and manage applications on Kubernetes using _charts_.
Charts are collections of Kubernetes manifests that describe an application, and can include templates, dependencies, and configuration options.
Helm makes it easy to deploy complex applications, and manage their lifecycle.
For example, to install [Grafana](https://grafana.com/) on your cluster

```sh
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
helm install my-release grafana/grafana
```

Kustomize is a tool for customizing Kubernetes YAML configurations.
It allows you to create overlays, which are modifications to existing Kubernetes manifests, without changing the original files.
This is useful for managing different environments, such as development, staging, and production, without duplicating YAML files.
In our app, we use Kustomize, though quite trivially.

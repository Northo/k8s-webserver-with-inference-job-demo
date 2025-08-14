# Copy-Paste

!!! info

    Here are some snippets for simple copy-paste.

## Simple example

!!! warning

    For simplicity, we did not include any namespace in the manifests.
    You should add this explicitly as a flag, like `kubectl apply -f <file> --namespace my-namespace`.

To run a simple nginx demo web server, we start a pod like
```yaml
# pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: hello-web
  labels:
    app: hello-web
spec:
  containers:
    - name: hello-web
      image: nginxdemos/hello:plain-text
      ports:
        - containerPort: 80
```

=== "`deployment.yaml`"

    ```yaml hl_lines="14-24"
    # deployment.yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: hello-web
      labels:
        app: hello-web
    spec:
      replicas: 2
      selector:
        matchLabels:
          app: hello-web
      template:
        metadata:
          labels:
            app: hello-web
        spec:
          containers:
            - name: hello-web
              image: nginxdemos/hello:plain-text
              ports:
                - containerPort: 80
    ```
    <div markdown class="result">

    !!! info "Notice how the highlighted section in the deployment, is exactly the same as the pod spec!"

    </div>

=== "`service.yaml`"

    ```yaml
    # service.yaml
    apiVersion: v1
    kind: Service
    metadata:
      name: hello-web
    spec:
      selector:
        app: hello-web
      ports:
        - port: 80
          targetPort: 80
          protocol: TCP
    ```

??? tip "Exposing publicly!"

    To expose our service outside the cluster, we'll make an ingress.
    ```yaml
    # ingress.yaml
    apiVersion: networking.k8s.io/v1
    kind: Ingress
    metadata:
      name: hello-web
    spec:
      ingressClassName: nginx
      rules:
        - host: demo-ingress.<yourname>.<IP>.sslip.io
          http:
            paths:
              - path: /
                pathType: Prefix
                backend:
                  service:
                    name: hello-web
                    port:
                      number: 80
    ```

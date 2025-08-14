# Exercises

!!! tip

    Remember to activate completions!

    ```sh
    source <(kubectl completion zsh)  # Modify as appropriate for other shells
    ```

## Verify access to cluster

To verify we have access to the cluster, we'll run

```sh
kubectl cluster-info
```
<div markdown class="result">

which should result in something like

```
Kubernetes control plane is running at https://xxx:443
CoreDNS is running at https://xxx:443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy
Metrics-server is running at https://xxx:443/api/v1/namespaces/kube-system/services/https:metrics-server:/proxy
```

</div>

and

```sh
kubectl get namespaces
```
which should list some namespaces.

## Create a pod running a demo web server

First, well create a namespace for ourselves:

```sh
kubectl create namespace <yourname>
```

We now create a pod in our namespace

!!! warning "Note the `---namespace <yourname>`"

`kubectl apply --namespace <yourname> -f pod.yaml` with
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

This will run a pod, which we can verify by `kubectl get pod --namespace <yourname>`, and you'll see something like
```
NAME        READY   STATUS    RESTARTS   AGE
hello-web   1/1     Running   0          13s
```

!!! tip "Setting default namespace"

    To avoid typing `--namespace <yourname>` all the time, you can run
    ```sh
    kubectl config set-context --current --namespace=<yourname>
    ```
## Access the web server

To access the web server, we need to expose it, meaning, createing a service for it.
While we would normally do this with a YAML manifest (which we will see later), for now, create one with the `kubectl expose` command.
If you did it correctly, you should now see something like this when listing services
```
kubectl get services
NAME        TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)   AGE
hello-web   ClusterIP   10.0.251.230   <none>        80/TCP    5s
```

!!! tip "Alternative names and abbreviations"

    In guides or when using the autocomplete, sometimes you will see different words used for the same thing.
    For example, services are sometimes abbreviated svc, as `kubectl get svc`.
    Deployments will sometimes be written as `deployments.apps`, etc.


However, even though it is now exposed, we still have no way of visiting the endpoint!
The service only makes the pod accessible internally on the cluster.
To access it from our machines, it must be exposed externally.
Later, we'll look at ingress, but for now, we'll simply port-forward the service:
```sh
kubectl --namespace <yourname> port-forward services/hello-web 8080:80
```
and visit it at <http://localhost:8080>.

## A better way with Deployments and Services

What we have made until now, has been more of a toy example.
In reality, one rarely create pods manually, but rather deployments.

### Clean up

First, clean up what we already made.
One could simply delete the entire namespace, but try instead to find all resources in the namespace, and delete them one by one, using commands like

- `kubectl get`
- `kubectl describe`
- `kubectl delete`

### Making our deployment and service

!!! info "Namespace"

    For brevity, we here omit the namespace argument.
    Make sure to either include it, set the current context, or add it to the manifest YAML files!

Copy the `deployment.yaml` and `service.yaml` from [the copy-paste page](./copy-paste.md), and apply them.

!!! tip

    If you want, you can have all resource definitions in the same `.yaml` file, separated with a `---`.
    However, it is common to separate it into files, for more granular apply/delete control and better organization.

Verify that there is a deployment and service in the namespace, and run `kubectl describe` on the deployment and corresponding replicaset.
Check with `kubectl get` that the pods are created and ready.

??? tip "Convenience heredocs"

    To avoid creating tons of files for simple operations, [heredocs](https://en.wikipedia.org/wiki/Here_document) can be convenient.
    Simply do
    ```sh
    kubectl apply -f - <<EOF
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
    EOF
    ```


### Exposing our app externally

There are several ways to expose apps externally.
They all have different strengths and weaknesses;
the interested reader can search for service types, and look at ClusterIP, NodePort, and LoadBalancer.

On our cluster, which is quite normal, we have an [ingress controller](https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/), allowing us to set up [ingresses](https://kubernetes.io/docs/concepts/services-networking/ingress/).
An ingress is essentially a proxy server, that takes many requests coming to the same public IP, and directing them to the appropriate internal service.

Ingresses are, as everything else in Kubernetes, set up usinga YAML manifest:

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

In the above example, we do a small trick.
Since we have no domain name pointing to our cluster yet, we use [`sslip.io`](sslip.io) as a DNS.
It simply resolves the IP address in front of `sslip.io`.

The IP address we put here, is the same as the one we would put into a domain name if we had one.
To find it, we need to find the public IP address of our ingress controller's load balancer[^1].

[^1]: If you did not understand that mouthful, don't worry!

How to find this, is an exercise for the reader.
Firstly, find the apprpriate namespace;
its name involves `ingress` and `nginx`.
Then, find a service of type `LoadBalancer`.
That load balancer's IP address, is the one to use.

!!! warning

    You are now looking into namespaces containing important internals of the cluster.
    If you have liberal permissions, thread carefully!
    `kubectl get` and `kubectl describe` is always safe, but do not use modifying commands.

Now, you can visit your app at `demo-ingress.<yourname>.<IP>.sslip.io`.

## Clean up

When you are finished, clean up everything by deleting your namespace.

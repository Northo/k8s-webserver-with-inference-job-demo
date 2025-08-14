# Presentation

Here are some instructions for what to set up (by the admin) on the presentation day.

## Auth for the dashboard

Create a namespace and service account, give it appropriate role, and create a token:

```sh
# choose a dedicated namespace (keeps things tidy)
kubectl create ns demo-access

# service account
kubectl -n demo-access create sa demo-admin

# cluster-wide superuser (be careful!)
cat <<'EOF' | kubectl apply -f -
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: demo-admin-cluster-admin
subjects:
- kind: ServiceAccount
  name: demo-admin
  namespace: demo-access
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
EOF

# short-lived token (e.g., 24h). Run again to refresh whenever you want.
kubectl -n demo-access create token demo-admin --duration=24h

```

## Auth for `kubectl`

Assuming the service account above is already created, do

```sh
SERVER=$(kubectl config view --raw -o jsonpath='{.clusters[0].cluster.server}')
CA_DATA=$(kubectl config view --raw -o jsonpath='{.clusters[0].cluster.certificate-authority-data}')
TOKEN=$(kubectl -n demo-access create token demo-admin --duration=24h)

cat > ./demo-admin.kubeconfig <<EOF
apiVersion: v1
kind: Config
clusters:
- name: demo-aks
  cluster:
    server: ${SERVER}
    certificate-authority-data: ${CA_DATA}
users:
- name: demo-admin
  user:
    token: ${TOKEN}
contexts:
- name: demo-admin@demo-aks
  context:
    cluster: demo-aks
    user: demo-admin
current-context: demo-admin@demo-aks
EOF
echo "Wrote ./demo-admin.kubeconfig"
```
and have uers use the `demo-admin.kubeconfig` as their config file, by doing `export KUBECONFIG=./demo-admin.kubeconfig`.

## Ingress for Grafana

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: grafana-ingress
  namespace: monitoring
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-production
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - grafana.4.210.9.109.sslip.io
    secretName: grafana-ingress-tls
  rules:
  - host: grafana.4.210.9.109.sslip.io
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: kube-prometheus-stack-grafana
            port:
              name: http-web
```

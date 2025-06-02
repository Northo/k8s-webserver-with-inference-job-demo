#!/bin/bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

cat << EOF
Run 'argocd admin initial-password -n argocd' to get the initial password for the admin user."

Run 'kubectl port-forward svc/argocd-server -n argocd 8080:443'
then login with 
'argocd login localhost:8080' username admin
EOF
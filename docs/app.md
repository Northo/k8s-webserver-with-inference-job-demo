# The sample app

The sample app we are making, is a simple static front end.
It allows the user to supply some input, which is handled by an API.
The API starts a job, which requires a GPU node, which will be allocated on demand.
The job will run a model inference, and return the result to the front end.

The components we need, are:

- A static front end, served by a web server
- An API server to handle requests
- A job that runs a model inference using a GPU node

In addition, we will use 

- ArgoCD for continuous deployment
- Argo Workflows for managing the job execution
- Azure Kubernetes Service (AKS) for hosting the Kubernetes cluster and managing node pools

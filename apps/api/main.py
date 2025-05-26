from fastapi import FastAPI, HTTPException
from kubernetes import client, config
import uuid

app = FastAPI()

# Load Kubernetes config (for in-cluster use)
config.load_incluster_config()
batch_v1 = client.BatchV1Api()

@app.post("/submit-job")
def submit_job():
    job_name = f"job-{uuid.uuid4().hex[:8]}"

    job = client.V1Job(
        metadata=client.V1ObjectMeta(name=job_name),
        spec=client.V1JobSpec(
            template=client.V1PodTemplateSpec(
                metadata=client.V1ObjectMeta(labels={"job": job_name}),
                spec=client.V1PodSpec(
                    containers=[client.V1Container(
                        name="hello",
                        image="busybox",
                        command=["/bin/sh", "-c", "echo Hello from Kubernetes Job && sleep 10"]
                    )],
                    restart_policy="Never",
                )
            ),
            ttl_seconds_after_finished=10,
        )
    )

    try:
        response = batch_v1.create_namespaced_job(namespace="default", body=job)
        return {"message": "Job submitted", "job_name": response.metadata.name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


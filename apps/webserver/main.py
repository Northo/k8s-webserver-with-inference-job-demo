from fastapi import FastAPI, UploadFile
from kubernetes import client, config
import shutil
import uuid

app = FastAPI()

def trigger_inference_job(file_id):
    config.load_incluster_config()  # or config.load_kube_config() locally
    batch_v1 = client.BatchV1Api()

    job_name = f"inference-job-{file_id}"

    job_manifest = {
        "apiVersion": "batch/v1",
        "kind": "Job",
        "metadata": {"name": job_name},
        "spec": {
            "template": {
                "spec": {
                    "containers": [{
                        "name": "stat-job",
                        "image": "myregistry.com/stat-job:latest",
                        "command": ["stat", f"/data/{file_id}.dat"],
                        "volumeMounts": [{"mountPath": "/data", "name": "data-volume"}],
                    }],
                    "volumes": [{"name": "data-volume", "persistentVolumeClaim": {"claimName": "data-pvc"}}],
                    "restartPolicy": "Never",
                    "nodeSelector": {"inference": "expensive"},
                }
            }
        }
    }

    batch_v1.create_namespaced_job(namespace="default", body=job_manifest)
    return job_name

@app.post("/upload/")
async def upload_and_trigger(file: UploadFile):
    file_id = str(uuid.uuid4())
    file_location = f"/data/{file_id}.dat"

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Trigger Kubernetes Job (next step)
    job_name = trigger_inference_job(file_id)

    return {"job_name": job_name}


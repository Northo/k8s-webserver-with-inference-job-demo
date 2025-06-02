from fastapi import FastAPI, HTTPException
import uuid
from hera.workflows import Workflow, WorkflowsService, Steps, script
from hera.workflows.models import WorkflowTemplateRef

app = FastAPI()



    # job = client.V1Job(
    #     metadata=client.V1ObjectMeta(name=job_name),
    #     spec=client.V1JobSpec(
    #         template=client.V1PodTemplateSpec(
    #             metadata=client.V1ObjectMeta(labels={"job": job_name}),
    #             spec=client.V1PodSpec(
    #                 containers=[
    #                     client.V1Container(
    #                         name="hello",
    #                         image="busybox",
    #                         command=[
    #                             "/bin/sh",
    #                             "-c",
    #                             "echo Hello from Kubernetes Job && sleep 10",
    #                         ],
    #                     )
    #                 ],
    #                 restart_policy="Never",
    #             ),
    #         ),
    #         ttl_seconds_after_finished=10,
    #     ),
    # )

    # try:
    #     response = batch_v1.create_namespaced_job(namespace="default", body=job)
    #     return {"message": "Job submitted", "job_name": response.metadata.name}
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))
    
@script()
def echo(message: str):
    print(message)

def main():
    with Workflow(
        generate_name="hello-world-",
        entrypoint="print-message",
        namespace="argo",
        workflows_service=WorkflowsService(host="https://localhost:2746", verify_ssl=False),
        workflow_template_ref=WorkflowTemplateRef(name="workflow-template-submittable"),
    ) as w:
        pass
        # with Steps(name="steps"):
        #     echo(arguments={"message": "Hello world!"})

    w.create()

@app.post("/submit-job")
def submit_job():
    main()

    
if __name__ == "__main__":
    main()

import os
import stat
from turtle import st
from fastapi import FastAPI
from hera.workflows import Workflow, WorkflowsService
from hera.workflows.models import (
    WorkflowTemplateRef,
    WorkflowStatus,
    ArtifactRepositoryRef,
)

app = FastAPI()
host = os.environ.get("ARGO_HOST", "https://localhost:2746")


def main(some_name: str) -> Workflow:
    with Workflow(
        generate_name="hello-world-",
        entrypoint="modify-message",
        namespace="argo",
        workflows_service=WorkflowsService(host=host, verify_ssl=False),
        workflow_template_ref=WorkflowTemplateRef(name="workflow-template-submittable"),
        arguments={"message": some_name},
    ) as w:
        pass

    w.create()
    return w


@app.post("/submit-job")
def submit_job(some_name: str) -> dict:
    w = main(some_name)
    return w.to_dict()


@app.get("/status")
def get_status(name: str) -> dict:
    status = (
        WorkflowsService(host=host, verify_ssl=False)
        .get_workflow(name=name, namespace="argo")
        .status
    )
    if status is None:
        return {"status": "Workflow not found"}

    return {"phase": status.phase}


@app.get("/get-outputs")
def get_outputs(name: str) -> str:
    status = (
        WorkflowsService(host=host, verify_ssl=False)
        .get_workflow(name=name, namespace="argo")
        .status
    )
    if status is None:
        return {"status": "Workflow not found"}

    return {
        "artifacts": [a.azure for a in status.outputs.artifacts]
        if status.outputs
        else None,
    }


if __name__ == "__main__":
    main()

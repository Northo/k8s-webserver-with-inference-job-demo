import os
from fastapi import FastAPI
from hera.workflows import Workflow, WorkflowsService, script
from hera.workflows.models import WorkflowTemplateRef

app = FastAPI()


@script()
def echo(message: str):
    print(message)


def main():
    host = os.environ.get("ARGO_HOST", "https://localhost:2746")

    with Workflow(
        generate_name="hello-world-",
        entrypoint="print-message",
        namespace="argo",
        workflows_service=WorkflowsService(host=host, verify_ssl=False),
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

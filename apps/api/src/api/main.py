import os
from datetime import datetime, timedelta
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from hera.workflows import Workflow, WorkflowsService
from hera.workflows.models import WorkflowTemplateRef
from azure.storage.blob import generate_blob_sas, BlobClient, BlobServiceClient
from azure.identity import DefaultAzureCredential

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


def _storage_account_name_from_endpoint(endpoint: str) -> str:
    # Extract the storage account name from the endpoint URL
    prefix = "https://"
    suffix = ".blob.core.windows.net"
    if endpoint.startswith(prefix) and endpoint.endswith(suffix):
        return endpoint[len(prefix) : -len(suffix)]
    raise ValueError("Invalid Azure Blob Storage endpoint format")


def _construct_blob_link(
    account_name: str,
    container: str,
    blob_name: str,
) -> str:
    return f"https://{account_name}.blob.core.windows.net/{container}/{blob_name}"

def _generate_blob_download_link(
    account_name: str,
    container: str,
    blob_name: str,
    credential,
) -> str:

    delegation_key = BlobServiceClient(
        account_url=f"https://{account_name}.blob.core.windows.net",
        credential=credential,
    ).get_user_delegation_key(
        key_start_time=datetime.now(),
        key_expiry_time=datetime.now() + timedelta(hours=1),
    )
    sas = generate_blob_sas(
        account_name=account_name,
        container_name=container,
        blob_name=blob_name,
        user_delegation_key=delegation_key,
        permission="r",
        expiry=datetime.now() + timedelta(hours=1),
    )
    return f"{_construct_blob_link(account_name, container, blob_name)}?{sas}"


@app.get("/get-outputs")
def get_outputs(name: str) -> dict:
    status = (
        WorkflowsService(host=host, verify_ssl=False)
        .get_workflow(name=name, namespace="argo")
        .status
    )
    if status is None:
        return JSONResponse(status_code=404, content={"status": "Workflow not found"})

    azure_repo_info = status.artifact_repository_ref.artifact_repository.azure
    azure_storage_account = _storage_account_name_from_endpoint(
        azure_repo_info.endpoint
    )

    return {
        "status": jsonable_encoder(status),
        "download_link": _generate_blob_download_link(
            azure_storage_account,
            azure_repo_info.container,
            status.outputs.artifacts[0].azure.blob,
            DefaultAzureCredential(),
        ),
    }


if __name__ == "__main__":
    main()

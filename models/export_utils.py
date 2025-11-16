import hashlib
import json
import os
import tempfile

import boto3
from botocore.exceptions import BotoCoreError, ClientError
import torch

from logger import get_logger


logger = get_logger(__name__)


def _calculate_sha256(file: str) -> str:
    logger.info(f"Calculating SHA256 for {file}")

    sha256_hash = hashlib.sha256()
    with open(file, "rb") as f:
        for block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(block)

    return sha256_hash.hexdigest()


def _upload_file_to_s3(file_path: str, bucket_name: str, object_key: str) -> None:
    """
    Uploads the specified file to an S3 bucket.

    Args:
        file_path (str): Path to the file on disk.
        bucket_name (str): Name of the S3 bucket.
        object_key (str): The S3 object key (path inside the bucket).
    """

    logger.info(f"Uploading {file_path} to s3://{bucket_name}/{object_key}")
    s3_client = boto3.client("s3")
    try:
        s3_client.upload_file(file_path, bucket_name, object_key)
        logger.info("Upload successful.")
    except (BotoCoreError, ClientError) as e:
        logger.error(f"Failed to upload {file_path} to S3: {e}")
        raise


def export_and_save(
    model: torch.nn.Module, inputs: tuple[torch.Tensor], model_id: str
):
    # Export the model
    exported_program = torch.export.export(model, inputs)

    organization, model_name = model_id.split("/")
    model_file_name = model_name + ".pt2"
    model_fx_name = model_name + ".fx"

    # Create temporary directory and store the exported model
    with tempfile.TemporaryDirectory() as output_tmp_path:
        model_file_path = os.path.join(output_tmp_path, model_file_name)
        model_fx_path = os.path.join(output_tmp_path, model_fx_name)
        
        torch.export.save(
            exported_program, model_file_path
        )

        with open(model_fx_path, "w") as f:
            f.write(exported_program.__str__())
        
        # Calculate SHA256 of the files
        model_file_sha256 = _calculate_sha256(model_file_path)
        model_fx_sha256 = _calculate_sha256(model_fx_path)

        # Upload the files to S3
        sleep(100)

    # Prepare model card
    model_card = {
        "model_id": model_id,
        "organization": organization
        "model_name": model_name,
        "input_sizes": [list(tensor.shape) for tensor in inputs],
        "model_file_name": model_file_name,
        "model_sha256": model_file_sha256,
        "fx_file_name": model_fx_name,
        "fx_sha256": model_dx_sha256
    }

    # Save model card to repo
    config_path = os.path.join(os.path.dirname(__file__), "configs", model_name)
    os.makedirs(config_path, exist_ok=True)

    json_path = os.path.join(config_path + ".json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(model_card, f, indent=4)

import hashlib
import json
import os

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


def export_and_save(
    model: torch.nn.Module, inputs: tuple[torch.Tensor], model_name: str
):
    # Export the model
    exported_program = torch.export.export(model, inputs)

    # Create temporary directory and store the exported model
    model_file_name = model_name.replace("/", "_") + ".pt2"
    with tempfile.TemporaryDirectory() as output_tmp_path:
        torch.export.save(
            exported_program, os.path.join(output_tmp_path, model_file_name)
        )

        # Calculate SHA256 of the model file
        model_file_sha256 = _calculate_sha256(
            os.path.join(output_tmp_path, model_file_name)
        )

    # Prepare model card
    model_card = {
        "model_name": model_name,
        "input_sizes": [list(tensor.shape) for tensor in inputs],
        "model_file_name": model_file_name,
        "sha256": model_file_sha256,
    }

    # Save model card to repo
    config_path = Path(__file__).parent / "configs" / model_name
    config_path.mkdir(exist_ok=True)

    json_path = config_path / "model_card.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(model_card, f, indent=4)

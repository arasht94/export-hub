import argparse
from transformers import AutoModelForCausalLM

import torch

from export_utils import export_and_save
from logger import get_logger


logger = get_logger(__name__)


def export_default_models():
    logger.info(f"Starting default model export process")

    models = [
        # "meta-llama/Meta-Llama-3-8B-Instruct",
        # "Qwen/Qwen3-1.7B",
        "DeepChem/ChemBERTa-100M-MLM"
    ]

    for model_name in models:
        logger.info(f"Instantiating model: {model_name}")
        model_instance = AutoModelForCausalLM.from_pretrained(model_name)
        inputs = (torch.randint(0, model_instance.config.vocab_size, (1, 1)),)
        export_and_save(model_instance, inputs, model_name)

    logger.info(f"Default models exported successfully!")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output_path", type=str, default="models")
    return parser.parse_args()


def main():
    args = parse_args()
    export_default_models(args.output_path)


if __name__ == "__main__":
    main()

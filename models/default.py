import argparse
from transformers import AutoModelForCausalLM

import torch

from export_utils import export_and_save


def export_default_models(output_path: str):
    models = [
        # "meta-llama/Meta-Llama-3-8B-Instruct",
        # "Qwen/Qwen3-1.7B",
        "DeepChem/ChemBERTa-100M-MLM"
    ]

    for model_name in models:
        model_instance = AutoModelForCausalLM.from_pretrained(model_name)
        inputs = (torch.randint(0, model_instance.config.vocab_size, (1, 1)),)
        export_and_save(model_instance, inputs, output_path, model_name)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output_path", type=str, default="models")
    return parser.parse_args()


def main():
    args = parse_args()
    export_default_models(args.output_path)


if __name__ == "__main__":
    main()

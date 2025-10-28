import os

from default import export_default_models


def export_all_models():
    output_path = "exported_models"
    os.makedirs(output_path, exist_ok=True)

    # Model export functions
    export_default_models(output_path)


if __name__ == "__main__":
    export_all_models()

import os

from default import export_default_models


os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"


def export_all_models():
    # Model export functions
    export_default_models()


if __name__ == "__main__":
    export_all_models()

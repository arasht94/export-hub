import os

import torch


def export_and_save(model: torch.nn.Module, inputs: tuple[torch.Tensor], path: str, model_name: str):
    
    exported_program = torch.export.export(model, inputs)
    
    model_name = model_name.replace("/", "_") + ".pt2"
    torch.export.save(exported_program, os.path.join(path, model_name))
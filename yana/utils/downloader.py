import torch
from pathlib import Path


def download_from_torch_hub(url: str, file: Path, progress: bool = True) -> None:
    """
    Downloads resources for torch hub

    parameters:
        url: The URL of the resource
        local_file: The path to the download location
        progress: Display progress while downloading

    returns:
        None
    """
    file = file.resolve()
    if not file.is_file():
        print(f"Downloading {file} from torch hub")
        torch.hub.download_url_to_file(url, str(file.resolve()), progress=progress)
    else:
        print(f"{file} already exists. Skipping download")

import os
from typing import Union, List

def get_files_by_ext(directory: str, 
                     media_extensions: Union[str, List[str]]
                     )-> List[str]:
    
    if isinstance(media_extensions, str):
        media_extensions = [media_extensions]

    relative_paths = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if any(file.endswith(ext) for ext in media_extensions):
                relative_path = os.path.relpath(os.path.join(root, file), 
                                                directory)
                relative_paths.append(relative_path)
    relative_paths = sorted(relative_paths)
    return relative_paths
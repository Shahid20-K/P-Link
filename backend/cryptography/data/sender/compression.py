"""
Function Name: compress_file
Purpose: Compress a file or folder (first archive using tarfile) using zstandard (.zst) compression.
Inputs:
    - path: Path to the file or folder to be compressed
    - output_dir: Directory where the compressed file will be stored
Outputs:
    - Returns the path of the compressed `.zst` file
"""
from pathlib import Path
import zstandard as zstd
import tarfile

from utils.logging import LogType, log

def compress_file(path, output_dir,general_logfile_path):
    p = Path(path)
    APP_COMPRESSED_DIR = Path(output_dir)
    APP_COMPRESSED_DIR.mkdir(parents=True, exist_ok=True)

    if not (p.is_file() or p.is_dir()):
        log("Unsupported path type",
            LogType.ERROR,
            "Failure",
            general_logfile_path,
            False
        )
        raise ValueError("Unsupported path type")

    tar_path = None

    if p.is_dir():
        tar_path = APP_COMPRESSED_DIR/(p.name + ".tar")
        with tarfile.open(tar_path, 'w') as tar:
            tar.add(p, arcname=p.name)
        p = tar_path
        log("Tarfile opened",
            LogType.INFO,
            "Success",
            general_logfile_path,
            False
        )

    compressed_path = APP_COMPRESSED_DIR/(p.name + ".zst")

    cctx = zstd.ZstdCompressor()
    with open(p, 'rb') as infile, open(compressed_path, 'wb') as outfile:
        cctx.copy_stream(infile, outfile)
    log("Tarfile Compressed",
        LogType.INFO,
        "Success",
        general_logfile_path,
        False
    )

    if tar_path and tar_path.exists():
        tar_path.unlink()

    log("File/Folder compressed succesfully",
        LogType.INFO,
        "Success",
        general_logfile_path,
        True
    )

    return compressed_path

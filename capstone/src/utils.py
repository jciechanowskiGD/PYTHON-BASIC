import logging
import os
import json

logging.basicConfig(
    level=logging.INFO, 
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ])
logger = logging.getLogger(__name__)

def clear_path(path_to_save_files: str, file_name: str, clear_path: bool) -> None:
    if not clear_path:
        return

    files = os.listdir(path_to_save_files)
    for file in files:
        if file.startswith(file_name):
            os.remove(f"{path_to_save_files}/{file}")
    logger.info("Deleted files that match base file_name")


def read_schema(path_or_schema: str) -> dict:
    if os.path.isfile(path_or_schema):
        try:
            with open(path_or_schema, "r") as f:
                schema = f.read()
                logger.info("Schema read from file")
                return json.loads(schema)
        except Exception:
            logger.error("Error while reading schema from file")
            exit()

    else:
        try:
            schema = json.loads(path_or_schema)
            logger.info("Schema read from cli")
            return schema
        except Exception:
            logger.error("Error while reading schema from input")
            exit()
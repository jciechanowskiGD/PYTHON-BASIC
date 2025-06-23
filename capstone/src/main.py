import argparse
import logging
import configparser
import os
from utils import read_schema, clear_path
from generator import DataGenerator

logging.basicConfig(
    level=logging.INFO, 
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ])
logger = logging.getLogger(__name__)


def parser_init() -> argparse.ArgumentParser:
    config = configparser.ConfigParser()
    config.read(f"{os.path.dirname(os.path.abspath(__file__))}/default.ini")

    logger.info("Initializing program")
    parser = argparse.ArgumentParser(
        prog="Capstone project",
        description="Capstone project for Python basic course",
    )
    parser.add_argument(
        "path_to_save_files", help="Where all files need to save", type=str
    )
    parser.add_argument(
        "--file_count",
        help="How much json files to generate",
        type=int,
        default=config["DEFAULT"]["file_count"],
    )
    parser.add_argument(
        "--file_name",
        help="Base file_name.",
        type=str,
        default=config["DEFAULT"]["file_name"],
    )
    parser.add_argument(
        "--file_prefix",
        choices=["count", "random", "uuid"],
        help="What prefix for file name to use if more than 1 file needs to be generated.",
        default=config["DEFAULT"]["file_prefix"],
    )
    parser.add_argument(
        "--data_schema",
        help="Its a string with json schema or json file",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--data_lines",
        help="Count of lines for each file.",
        type=int,
        default=config["DEFAULT"]["data_lines"],
    )
    parser.add_argument(
        "--clear_path",
        help="If this flag is on, before the script starts creating new data files, all files in path_to_save_files that match file_name will be deleted.",
        action="store_true",
    )
    parser.add_argument(
        "--multiprocessing",
        help="The number of processes used to create files.",
        type=int,
        default=config["DEFAULT"]["multiprocessing"],
    )

    return parser


def main():
    parser = parser_init()
    args = parser.parse_args()

    if os.path.isfile(args.path_to_save_files):
        logger.error("Path to file")
        exit()
    if not os.path.exists(args.path_to_save_files):
        os.mkdir(args.path_to_save_files)

    logger.info("Clearing path...")
    clear_path(args.path_to_save_files, args.file_name, args.clear_path)
    
    logger.info("Reading schema...")
    schema = read_schema(args.data_schema)

    generator = DataGenerator()
    logger.info("Generating data...")
    generator.generate_data(
        schema,
        args.data_lines,
        args.multiprocessing,
        args.file_count,
        args.path_to_save_files,
        args.file_name,
        args.file_prefix,
    )


if __name__ == "__main__":
    main()
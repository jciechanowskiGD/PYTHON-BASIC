import argparse
import logging
import random
import uuid
import configparser
import time
import os
from multiprocessing import Pool
import json

logger = logging.getLogger(__name__)


def clear_path(path_to_save_files: str, file_name: str, clear_path: bool) -> None:
    if not clear_path:
        return

    files = os.listdir(path_to_save_files)
    logger.info("Begining deletion of files that match base file_name")
    for file in files:
        if file.startswith(file_name):
            os.remove(f"{path_to_save_files}/{file}")
    logger.info("Deleted files that match base file_name")


def generate_file_paths(
    path_to_save_file: str, file_name: str, file_prefix: str, file_count: int
) -> list:
    if file_count < 0:
        logger.error("Files count cant be less than 0")
        exit()
    elif file_count == 0:
        return []
    elif file_count == 1:
        return [f"{path_to_save_file}/{file_name}"]
    if file_prefix == "count":
        return [f"{path_to_save_file}/{file_name}{i}" for i in range(file_count)]
    elif file_prefix == "random":
        return [
            f"{path_to_save_file}/{file_name}{random.randint(1, 10000000)}"
            for _ in range(file_count)
        ]
    elif file_prefix == "uuid":
        return [
            f"{path_to_save_file}/{file_name}{uuid.uuid4()}" for _ in range(file_count)
        ]
    logger.error("Wrong prefix")
    exit()


def save_to_file(file_path: str, data: str) -> None:
    with open(f"{file_path}.json", "w") as f:
        json.dump(data, f)
    logger.info(f"Saved to file {file_path}.json")


def _generate_data_int(right_part: str) -> int:
    logger.info("Generating data for int")
    # rand empty
    if right_part.endswith("rand"):
        return random.randint(0, 10000)

    # rand with vals
    elif right_part[4:8] == "rand":
        ints_s = right_part[9:-1].split(",")
        ints = [i.strip() for i in ints_s]
        try:
            i1, i2 = int(ints[0]), int(ints[1])
            return random.randint(i1, i2)
        except Exception as e:
            logger.error("Exception when trying to convert to int")
            exit()

    # empty
    elif right_part.endswith("int") or right_part.endswith("int:"):
        return None

    # list
    elif right_part[4] == "[" and right_part.endswith("]"):
        ints = right_part[4:-1].replace("'", '"')
        ints = json.loads(ints)
        try:
            ints = [int(i) for i in ints]
            return random.choice(ints)
        except Exception as e:
            logger.error("Not all values are int")
            exit()

    # any other
    else:
        try:
            i = int(right_part[4:].strip())
            return i
        except Exception as e:
            logger.error("Invalid value after int:")
            exit()


def _generate_data_str(right_part: str) -> str:
    logger.info("Generating data for string")
    # rand
    if right_part.endswith("rand"):
        return str(uuid.uuid4())
    # list
    elif right_part[4] == "[" and right_part.endswith("]"):
        vals = right_part[4:].replace("'", '"')
        vals = json.loads(vals)
        return random.choice(vals)
    elif right_part.startswith("str") or right_part.startswith("str:"):
        return ""
    else:
        return right_part[4:]


def _generate_data_timestamp(right_part: str, already_warned=[]) -> float:
    if len(right_part) > 10 and not already_warned:
        already_warned.append(1)
        logger.warning('In time stamp values after ":" will be ignored')

    return time.time()


def generate_data_line(data_schema: dict[str, str]) -> dict:
    data = {}

    for k in data_schema:
        if data_schema[k].startswith("int"):
            data[k] = _generate_data_int(data_schema[k])
        elif data_schema[k].startswith("timestamp"):
            data[k] = _generate_data_timestamp(data_schema[k])
        elif data_schema[k].startswith("str"):
            logger.info(f"data_schema[k]")
            data[k] = _generate_data_str(data_schema[k])
        else:
            logger.error(f"Type not supported {data_schema[k]}")
            exit()

    return data


def create_file_content(data_schema: dict, data_lines: int):
    all_lines = []
    for _ in range(data_lines):
        data_line = generate_data_line(data_schema)
        all_lines.append(data_line)
    data = json.dumps(all_lines)
    return data


def file_generation_helper(data_schema: dict, data_lines: int, file_path: str):
    data = create_file_content(data_schema, data_lines)
    save_to_file(file_path, data)


def generate_data(
    data_schema: str,
    data_lines: int,
    max_workers: int,
    file_count: int,
    path_to_save_files: str,
    file_name: str,
    file_prefix: str,
):
    if max_workers <= 0:
        logger.error("We can use <= 0 cores")
        exit()
    file_paths = generate_file_paths(
        path_to_save_files, file_name, file_prefix, file_count
    )
    params = [(data_schema, data_lines, file_path) for file_path in file_paths]
    logger.info("Data generating...")
    if len(file_paths) == 0:
        print(create_file_content(data_schema, data_lines))
        return

    if max_workers > os.cpu_count():
        max_workers = os.cpu_count()

    with Pool(processes=max_workers) as pool:
        pool.starmap(file_generation_helper, params)
    logger.info("Data generated")


def read_schema(path_or_schema: str) -> dict:
    if os.path.isfile(path_or_schema):
        try:
            with open(path_or_schema, "r") as f:
                schema = json.load(f)
                return schema
        except Exception:
            logger.error("Error while reading schema from file")
            exit()
    else:
        try:
            schema = json.loads(path_or_schema)
            return schema
        except Exception:
            logger.error("Error while reading schema from input")
            exit()


def parser_init() -> argparse.ArgumentParser:
    config = configparser.ConfigParser()
    config.read("./src/default.ini")

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


# prefix is still todo
def main():
    parser = parser_init()
    args = parser.parse_args()

    if os.path.isfile(args.path_to_save_files):
        logger.error("Path to file")
        exit()
    if not os.path.exists(args.path_to_save_files):
        os.mkdir(args.path_to_save_files)

    clear_path(args.path_to_save_files, args.file_name, args.clear_path)
    schema = read_schema(args.data_schema)

    generate_data(
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

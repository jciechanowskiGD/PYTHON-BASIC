import pytest
from src import generator, utils
from unittest.mock import patch
import time
import os
import subprocess

# TESTS for data types

paramets_int = [
    ("int:", [None]),
    ("int", [None]),
    ("int:rand", [i for i in range(0, 10001)]),
    ("int:[1,2,3]", [1, 2, 3]),
    ("int:rand(1,10)", [i for i in range(1, 11)]),
]

@pytest.mark.parametrize("x, exp", paramets_int)
def test_type_int(x, exp):
    gen = generator.DataGenerator()
    assert gen._generate_data_int(x) in exp


paramets_str = [
    ("str:", [""]),
    ("str", [""]),
    ("str:rand", ["3a9829d9-caf8-4313-ae9a-03273288f3ec"]),
    ('str:["1","2","3"]', ["1", "2", "3"]),
]

@pytest.mark.parametrize("x, exp", paramets_str)
@patch("uuid.uuid4", return_value="3a9829d9-caf8-4313-ae9a-03273288f3ec")
def test_type_str(mocked, x, exp):
    gen = generator.DataGenerator()
    assert gen._generate_data_str(x) in exp


t = time.time()
paramets_str = [
    ("timestamp:", t),
    ("timestamp", t),
    ("timestamp:rand", t),
    ('timestamp:xyz', t),
]

@pytest.mark.parametrize("x, exp", paramets_str)
@patch("time.time", return_value=t)
def test_type_timestamp(mocked, x, exp):
    gen = generator.DataGenerator()
    assert gen._generate_data_timestamp(x) == exp

# TESTS for data schemas

schemas = [
    ({"date": "timestamp:","name": "str:xyz"}, {"date": t, "name": "xyz"}),
    ({"int": "str:hello","date": "timestamp:"}, {"int": "hello", "date": t}),
    ({"name": "str:lala","num": "int:10"}, {"name": "lala", "num": 10}),
    ({"name": "str:hello","date": "timestamp:", "num": "int:"}, {"name": "hello", "date": t, "num": None}),
    ]

@pytest.mark.parametrize("x, exp", schemas)
@patch("time.time", return_value=t)
def test_schemas(mocked, x, exp):
    gen = generator.DataGenerator()
    assert gen.generate_data_line(x) == exp

# TESTS for schema_from_file 

def test_schema_from_file(tmp_path):
    file_name = 'schema.json'
    path = tmp_path / file_name
    schema = '{"name": "str:lala","num": "int:10"}'
    path.write_text(schema)
    assert utils.read_schema(path) == {"name": "str:lala", "num":"int:10"}
    

# TESTS for clear_path

def test_clear_path(tmp_path):
    file_name = 'file3.json'
    path = tmp_path / file_name
    path.write_text("1")
    assert len(os.listdir(tmp_path)) > 0
    base_file_name = 'file'
    utils.clear_path(tmp_path,base_file_name,True)
    assert len(os.listdir(tmp_path)) == 0

# TESTS for file creation

def file_saving(tmp_path):
    data = "{\"date\": 1750195416.063435, \"name\": \"bfd14841-49fa-4ce8-9444-4fa0cca49bbb\", \"type\": \"partner\", \"age\": 565}"
    path = tmp_path/'file1.json'
    gen = generator.DataGenerator()
    gen._save_to_file(path,data)
    assert os.path.exists(path)
    with open(path, 'r') as f:
        assert f.read() == "{\"date\": 1750195416.063435, \"name\": \"bfd14841-49fa-4ce8-9444-4fa0cca49bbb\", \"type\": \"partner\", \"age\": 565}"
    
# TESTS for to check a number of created files if “multiprocessing” > 1

def test_file_count(tmp_path):
    script_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/src/main.py"
    print(script_path)
    subprocess.run(['python3', 
                    script_path, 
                    tmp_path, 
                    '--file_count=12', 
                    '--multiprocessing=4', 
                    "--data_schema={\"date\": \"timestamp:\",\"name\": \"str:rand\",\"type\": \"str:['client', 'partner', 'government']\",\"age\": \"int:rand(100, 900)\"}",
                    '--clear_path'])
    assert len(os.listdir(tmp_path)) == 12

# My own test
@patch("uuid.uuid4", side_effect=["3a9829d9-caf8-4313-ae9a-03273288f3ec", "14b4f416-fa6e-4a03-aef4-b0fd1364cefd"])
@patch("random.randint", side_effect=["99", "1112"])
def test_file_paths(mock, mock2, tmp_path):
    base_file_name = 'file'
    gen = generator.DataGenerator()
    assert gen._generate_file_paths(tmp_path, base_file_name, 'uuid', 2) == [f'{tmp_path}/{base_file_name}3a9829d9-caf8-4313-ae9a-03273288f3ec', f'{tmp_path}/{base_file_name}14b4f416-fa6e-4a03-aef4-b0fd1364cefd']

    assert gen._generate_file_paths(tmp_path, base_file_name, 'count', 2) == [f'{tmp_path}/{base_file_name}0', f'{tmp_path}/{base_file_name}1']

    assert gen._generate_file_paths(tmp_path, base_file_name, 'random', 2) == [f'{tmp_path}/{base_file_name}99', f'{tmp_path}/{base_file_name}1112']
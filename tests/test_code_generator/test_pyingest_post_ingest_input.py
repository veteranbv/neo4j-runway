from typing import List
import unittest

from neo4j_runway.models import Node, Relationship, Property, DataModel
from neo4j_runway.code_generation import PyIngestConfigGenerator


nodes = [
    Node(
        label="NodeA",
        properties=[
            Property(name="alpha", type="str", csv_mapping="au", is_unique=True)
        ],
        csv_name="CSV_A",
    ),
    Node(
        label="NodeC",
        properties=[
            Property(name="gamma", type="str", csv_mapping="cu", is_unique=True),
            Property(name="decorator", type="str", csv_mapping="dec", is_unique=False),
        ],
        csv_name="CSV_A",
    ),
]
rel = Relationship(
    type="REL_AC", source="NodeA", target="NodeC", properties=[], csv_name="CSV_A"
)

data_model = DataModel(nodes=nodes, relationships=[rel])


class TestIngestPostIngestInput(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.maxDiff = None

    def test_post_ingest_generation_from_string_a(self) -> None:
        post_ingest: str = (
            "create (t:Test)\nset t.var = 1;\ncreate (t:Test2)\nset t.var = 2;"
        )
        gen = PyIngestConfigGenerator(
            data_model=data_model, file_directory="./", post_ingest_code=post_ingest
        )
        res = gen.generate_config_string()
        self.assertEqual(res, ans)

    def test_post_ingest_generation_from_string_b(self) -> None:
        post_ingest: str = """create (t:Test)
set t.var = 1;
create (t:Test2)
set t.var = 2;"""
        gen = PyIngestConfigGenerator(
            data_model=data_model, file_directory="./", post_ingest_code=post_ingest
        )
        res = gen.generate_config_string()
        self.assertEqual(res, ans)

    def test_post_ingest_generation_from_cypher_file(self) -> None:
        post_ingest_file_path: str = (
            "tests/resources/cypher/pyingest_post_ingest.cypher"
        )
        gen = PyIngestConfigGenerator(
            data_model=data_model,
            file_directory="./",
            post_ingest_code=post_ingest_file_path,
        )
        res = gen.generate_config_string()
        self.assertEqual(res, ans)

    def test_post_ingest_generation_from_cql_file(self) -> None:
        post_ingest_file_path: str = "tests/resources/cypher/pyingest_post_ingest.cql"
        gen = PyIngestConfigGenerator(
            data_model=data_model,
            file_directory="./",
            post_ingest_code=post_ingest_file_path,
        )
        res = gen.generate_config_string()
        self.assertEqual(res, ans)

    def test_post_ingest_generation_from_list(self) -> None:
        post_ingest: List[str] = [
            "create (t:Test)\nset t.var = 1",
            "create (t:Test2)\nset t.var = 2",
        ]
        gen = PyIngestConfigGenerator(
            data_model=data_model, file_directory="./", post_ingest_code=post_ingest
        )
        res = gen.generate_config_string()
        self.assertEqual(res, ans)


ans = """server_uri: None
admin_user: None
admin_pass: None
database: None
basepath: ./

pre_ingest:
  - CREATE CONSTRAINT nodea_alpha IF NOT EXISTS FOR (n:NodeA) REQUIRE n.alpha IS UNIQUE;
  - CREATE CONSTRAINT nodec_gamma IF NOT EXISTS FOR (n:NodeC) REQUIRE n.gamma IS UNIQUE;
files:
- chunk_size: 100
  cql: |
    WITH $dict.rows AS rows
    UNWIND rows AS row
    MERGE (n:NodeA {alpha: row.au})
  url: $BASE/./CSV_A.csv
- chunk_size: 100
  cql: |-
    WITH $dict.rows AS rows
    UNWIND rows AS row
    MERGE (n:NodeC {gamma: row.cu})
    SET n.decorator = row.dec
  url: $BASE/./CSV_A.csv
- chunk_size: 100
  cql: |
    WITH $dict.rows AS rows
    UNWIND rows as row
    MATCH (source:NodeA {alpha: row.au})
    MATCH (target:NodeC {gamma: row.cu})
    MERGE (source)-[n:REL_AC]->(target)
  url: $BASE/./CSV_A.csv

post_ingest:
  - create (t:Test)
    set t.var = 1
  - create (t:Test2)
    set t.var = 2
"""

if __name__ == "__main__":
    unittest.main()

people_pets_yaml_string = """
server_uri: bolt://localhost:7687
admin_user: neo4j
admin_pass: password
database: peoplepets
basepath: file:./

pre_ingest:
  - CREATE CONSTRAINT person_name IF NOT EXISTS FOR (n:Person) REQUIRE n.name IS UNIQUE;
  - CREATE CONSTRAINT toy_name IF NOT EXISTS FOR (n:Toy) REQUIRE n.name IS UNIQUE;
files:
- chunk_size: 100
  cql: |-
    WITH $dict.rows AS rows
    UNWIND rows AS row
    MERGE (n:Person {name: row.name})
    SET n.age = row.age
  url: $BASE/resources/data/people-pets.csv
- chunk_size: 100
  cql: |-
    WITH $dict.rows AS rows
    UNWIND rows AS row
    MERGE (target:Address{city: row.city, street: row.street})
  url: $BASE/resources/data/people-pets.csv
- chunk_size: 100
  cql: |-
    WITH $dict.rows AS rows
    UNWIND rows AS row
    MERGE (n:Pet {name: row.pet_name})
    SET n.kind = row.pet
  url: $BASE/resources/data/people-pets.csv
- chunk_size: 100
  cql: |-
    WITH $dict.rows AS rows
    UNWIND rows AS row
    MERGE (n:Toy {name: row.toy})
    SET n.kind = row.toy_type
  url: $BASE/resources/data/people-pets.csv
- chunk_size: 100
  cql: |-
    WITH $dict.rows AS rows
    UNWIND rows as row
    MATCH (source:Person{name: row.name})
    MATCH (target:Address{city: row.city, street: row.street})
    MERGE (source)-[n:HAS_ADDRESS]->(target)
  url: $BASE/resources/data/people-pets.csv
- chunk_size: 100
  cql: |-
    WITH $dict.rows AS rows
    UNWIND rows as row
    MATCH (source:Person{name:row.name})
    MATCH (target:Pet{name: row.pet_name})
    MERGE (source)-[n:HAS_PET]->(target)
  url: $BASE/resources/data/people-pets.csv
- chunk_size: 100
  cql: |-
    WITH $dict.rows AS rows
    UNWIND rows as row
    MATCH (source:Pet{name: row.pet_name})
    MATCH (target:Toy{name: row.toy})
    MERGE (source)-[n:PLAYS_WITH]->(target)
  url: $BASE/resources/data/people-pets.csv
- chunk_size: 100
  cql: |-
    WITH $dict.rows AS rows
    UNWIND rows as row
    MATCH (source:Person {name: row.name})
    MATCH (target:Person {name: row.knows})
    MERGE (source)-[n:KNOWS]->(target)
  url: $BASE/resources/data/people-pets.csv
"""

people_pets_multi_csv_yaml_string = """server_uri: bolt://localhost:7687
admin_user: neo4j
admin_pass: password
database: peoplepets
basepath: ./

pre_ingest:
  - CREATE CONSTRAINT person_name IF NOT EXISTS FOR (n:Person) REQUIRE n.name IS UNIQUE;
  - CREATE CONSTRAINT address_city_street IF NOT EXISTS FOR (n:Address) REQUIRE (n.city, n.street) IS NODE KEY;
  - CREATE CONSTRAINT pet_name IF NOT EXISTS FOR (n:Pet) REQUIRE n.name IS UNIQUE;
  - CREATE CONSTRAINT toy_name IF NOT EXISTS FOR (n:Toy) REQUIRE n.name IS UNIQUE;
  - CREATE CONSTRAINT shelter_name IF NOT EXISTS FOR (n:Shelter) REQUIRE n.name IS UNIQUE;
files:
- chunk_size: 100
  cql: |-
    WITH $dict.rows AS rows
    UNWIND rows AS row
    MERGE (n:Person {name: row.name})
    SET n.age = row.age
  url: $BASE/tests/resources/data/pets.csv
- chunk_size: 100
  cql: |
    WITH $dict.rows AS rows
    UNWIND rows AS row
    MERGE (n:Address {city: row.city, street: row.street})
  url: $BASE/tests/resources/data/pets.csv
- chunk_size: 100
  cql: |-
    WITH $dict.rows AS rows
    UNWIND rows AS row
    MERGE (n:Pet {name: row.pet_name})
    SET n.kind = row.pet
  url: $BASE/tests/resources/data/pets.csv
- chunk_size: 100
  cql: |-
    WITH $dict.rows AS rows
    UNWIND rows AS row
    MERGE (n:Toy {name: row.toy})
    SET n.kind = row.toy_type
  url: $BASE/tests/resources/data/pets.csv
- chunk_size: 100
  cql: |
    WITH $dict.rows AS rows
    UNWIND rows AS row
    MERGE (n:Shelter {name: row.shelter_name})
  url: $BASE/tests/resources/data/shelters.csv
- chunk_size: 100
  cql: |
    WITH $dict.rows AS rows
    UNWIND rows as row
    MATCH (source:Person {name: row.name})
    MATCH (target:Address {city: row.city, street: row.street})
    MERGE (source)-[n:HAS_ADDRESS]->(target)
  url: $BASE/tests/resources/data/pets.csv
- chunk_size: 100
  cql: |
    WITH $dict.rows AS rows
    UNWIND rows as row
    MATCH (source:Person {name: row.name})
    MATCH (target:Pet {name: row.pet_name})
    MERGE (source)-[n:HAS_PET]->(target)
  url: $BASE/tests/resources/data/pets.csv
- chunk_size: 100
  cql: |
    WITH $dict.rows AS rows
    UNWIND rows as row
    MATCH (source:Pet {name: row.pet_name})
    MATCH (target:Toy {name: row.toy})
    MERGE (source)-[n:PLAYS_WITH]->(target)
  url: $BASE/tests/resources/data/pets.csv
- chunk_size: 100
  cql: |
    WITH $dict.rows AS rows
    UNWIND rows as row
    MATCH (source:Pet {name: row.pet_name})
    MATCH (target:Shelter {name: row.shelter_name})
    MERGE (source)-[n:FROM_SHELTER]->(target)
  url: $BASE/tests/resources/data/shelters.csv
- chunk_size: 100
  cql: |
    WITH $dict.rows AS rows
    UNWIND rows as row
    MATCH (source:Shelter {name: row.shelter_name})
    MATCH (target:Address {city: row.city, street: row.street})
    MERGE (source)-[n:HAS_ADDRESS]->(target)
  url: $BASE/tests/resources/data/shelters.csv
- chunk_size: 100
  cql: |
    WITH $dict.rows AS rows
    UNWIND rows as row
    MATCH (source:Person {name: row.name})
    MATCH (target:Person {name: row.knows})
    MERGE (source)-[n:KNOWS]->(target)
  url: $BASE/tests/resources/data/pets.csv
"""

# Vertica Local Environment Preperation Scripts
###### A collection of scripts to aid in setting up a local testing environment emulating a production Vertica environment
***
### Installation
```
$ git clone https://github.com/jicuss/vertica_parity_env.git
$ pip install -e .[dev]
```


### Workflow Dependency Parser
This script looks through a workflow folder and parses out all tables referenced, inserted into, or updated. This will help you identify the origination source of the data and the destination tables it’s written into.

Example. Take a situation where you have a folder containing several SQL files that you will be working on. You don’t know which tables they are grabbing data from or updating. You can easily derive that information.

```
$ parse_workflow -w /fullpath/to/workflow
```

This command will parse the accessed tables and generate an output file in JSON format similar to this:

```json
[
    {
        "accessed": [
            "ExampleSchema.table_a",
            "ExampleSchema.table_b",
        ],
        "directory": "/a_workflow_folder/sql",
        "filename": "first_sql_file.sql",
        "modified": [
            "ExampleSchema.table_c"
        ]
    }
]
```

### VSQL Command Generator
Generates commands to copy data from one environment to another.

Modify the default credentials in config/default_credentials.json

You’ll need to make an input JSON file to declare which data you want to copy. There is an optional condition key. If the condition is declared (either as a string or an array of conditions) it will be added to the select statement generated. Here is an example of the declaration JSON file.

```
{
    "tables": [
        {"name": "ExampleSchema.table_a" },
        {
            "conditions": [
                "auth_id in (select auth_id from ExampleSchema_WS.table_c)",
                "auth_id = 5"
            ],
            "name": "ExampleSchema.table_b"
        }
    ]
}
```

Protip: You can generate an example JSON input file using the command
```
$ generate_example_copy_json
```

To generate the actual copy commands run something similar to

```
$ create_copy_commands -j table_copy.json
```

This will output schema copy commands similar to this:

```
vsql -U __USERNAME__ -w __PASSWORD__ -h Host  -d Analytics -At -F $'\t' -c "SELECT  *  from EXAMPLESCHEMA.TABLE_A ;"  > EXAMPLESCHEMA.TABLE_A.data
vsql -U __USERNAME__ -w __PASSWORD__ -h Host  -d Analytics -At -F $'\t' -c "SELECT  *  from EXAMPLESCHEMA.TABLE_B WHERE auth_id in (select auth_id from ExampleSchema_WS.table_c) AND auth_id = 5;"  > EXAMPLESCHEMA.TABLE_B.data

cat EXAMPLESCHEMA.TABLE_A.data | vsql -U dbadmin -w intuit01 -h 172.16.159.128 -d Analytics -c "COPY EXAMPLESCHEMA.TABLE_A  FROM STDIN DELIMITER E'\011';"
cat EXAMPLESCHEMA.TABLE_B.data | vsql -U dbadmin -w intuit01 -h 172.16.159.128 -d Analytics -c "COPY EXAMPLESCHEMA.TABLE_B  FROM STDIN DELIMITER E'\011';"

```



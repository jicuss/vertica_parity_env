# vertica_parity_env
a collection of scripts to aid in setting up a local testing environment emulating a production Vertica environment


# Workflow Dependency Parser
This script looks through a workflow folder and parses out all tables referenced, inserted into, or updated.
This will help you identify the origination source of the data and the destination tables its written into.

# VSQL Command Generator
Generates commands to copy data from one environment to another.

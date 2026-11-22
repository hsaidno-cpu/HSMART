# Contract validation tests

Run the local contract suite with:

~~~bash
python -m pytest -q
~~~

The suite currently covers:
- Capability manifest schema validity.
- A valid deterministic demo manifest fixture.
- Rejection of a manifest missing required fields.
- Rejection of unknown top-level manifest properties.
- Event envelope schema validity.
- A valid registry event fixture.
- Rejection of an event missing its required producer.
- OpenAPI 3.1 validation and required capability-discovery/invocation contract checks.

These are schema and document-contract tests. They do not test a Registry service, authentication, authorization, REST/MCP server, queue, worker, runtime isolation, synchronization, rollback or production operations. Those tests must be added when the corresponding implementation exists.

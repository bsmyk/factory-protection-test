# Repo-specific agents

A file here named after a kit agent replaces it. Add `extends: <kit agent>` to its front matter
to inherit everything and change only some settings, or append extra rules below the front matter:

    ---
    extends: reviewer
    ---
    Also check that every new endpoint has a rate limit.

A file with a new name defines a new agent. Give it `picks: <column>`, wire it in by pointing
another agent's `on_success` at that column, and add it to `agents =` in factory.conf.
See the kit's agents/examples/ folder.

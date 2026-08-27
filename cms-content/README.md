# CMS content drafts

This directory contains the source records to copy into Daniel's manifest repository after review.

Each cookbook has the required three-file contract:

- `index.md`: catalog metadata and the rendered recipe page
- `prompt.md`: a short instruction for a coding agent to set up and run the linked recipe
- `eval.json`: internal evaluation metadata

Five entries link directly to existing directories in `nebius/serverless-ai-cookbook`. SmolVLA links to the new template in this repository.

All entries intentionally remain `in_review`. The current evaluator only supports text-only Token Factory targets and cannot provision Nebius Serverless resources, so these evals remain disabled. Endpoint prices are shown as approximate active hourly rates in prose; job prices remain approximate per-run figures. Because the current CMS schema exposes only `estimated_cost_per_run_usd`, the endpoint structured-cost fields remain empty until the schema gains a cost unit. Publication and verification timestamps remain empty until controlled live runs provide evidence.

No generated Directus files from Daniel's repository are stored here.

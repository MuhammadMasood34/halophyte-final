# Halophyte Knowledge Graph source

This module retains the curated paper corpus, graph data, and reproducible graph-analysis scripts used by the browser-ready knowledge graph at `public/modules/knowledge-graph/index.html`.

- `data/papers.py` — curated literature records.
- `scripts/build_graph.py` — creates graph data from the corpus.
- `scripts/gap_analysis.py` — calculates graph-based research-gap candidates.
- `data/graph.json` and `data/kg_data.json` — checked-in graph datasets.

The integrated query panel searches the checked-in corpus locally and links results to paper identifiers; it does not require an external model API or secret.

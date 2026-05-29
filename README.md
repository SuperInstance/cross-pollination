# cross-pollination

Finds synergies between knowledge domains — a Python engine that discovers cross-room concept overlaps and recommends collaboration opportunities.

## What This Gives You

- **Concept extraction** — TF-IDF-lite keyword extraction from text
- **Synergy detection** — identifies overlapping concepts between knowledge domains
- **Overlap scoring** — quantitative measure of domain similarity
- **Recommendations** — suggests collaboration paths between domains

## Quick Start

```bash
pip install -e .

from cross_pollination.engine import ConceptExtractor, Synergy

extractor = ConceptExtractor(max_terms=50)
extractor.fit(["machine learning uses neural networks", "biology uses neural pathways"])
# Extract concepts and find cross-domain synergies
```

## How It Fits

Part of the Cocapn Fleet knowledge management pipeline. Part of the SuperInstance ecosystem.

Related repos:
- [cocapn-plato](https://github.com/SuperInstance/cocapn-plato) — PLATO framework
- [cocapn-curriculum](https://github.com/SuperInstance/cocapn-curriculum) — curriculum management
- [cocapn-worldmodel](https://github.com/SuperInstance/cocapn-worldmodel) — world modeling

## License

Apache 2.0

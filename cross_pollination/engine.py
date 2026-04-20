"""Cross-pollination engine — finds synergies between knowledge domains."""
import math
import re
from collections import Counter
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional, Set


def _tokenize(text: str) -> List[str]:
    return re.sub(r'[^a-z0-9 ]', '', text.lower()).split()


@dataclass
class Synergy:
    """A cross-room synergy opportunity."""
    room_a: str
    room_b: str
    shared_concepts: List[str]
    overlap_score: float
    recommendation: str = ""

    def __str__(self):
        return f"{self.room_a} ↔ {self.room_b} ({self.overlap_score:.2f}: {', '.join(self.shared_concepts[:5])})"


class ConceptExtractor:
    """Extract key terms from text using TF-IDF-lite."""

    def __init__(self, max_terms: int = 50, min_length: int = 3):
        self.max_terms = max_terms
        self.min_length = min_length
        self._doc_freq: Counter = Counter()
        self._doc_count: int = 0

    def fit(self, documents: List[str]) -> 'ConceptExtractor':
        self._doc_count = len(documents)
        self._doc_freq = Counter()
        for doc in documents:
            tokens = set(_tokenize(doc))
            for t in tokens:
                if len(t) >= self.min_length:
                    self._doc_freq[t] += 1
        return self

    def extract(self, text: str) -> List[Tuple[str, float]]:
        tokens = _tokenize(text)
        tf = Counter(t for t in tokens if len(t) >= self.min_length)
        if not tf or self._doc_count == 0:
            return []
        results = []
        for term, count in tf.items():
            tf_score = count / len(tokens)
            idf = math.log(self._doc_count / (self._doc_freq.get(term, 0) + 1))
            results.append((term, tf_score * idf))
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:self.max_terms]


class RoomGraph:
    """Graph of rooms connected by shared concepts."""

    def __init__(self):
        self.rooms: Dict[str, Set[str]] = {}
        self.edges: Dict[Tuple[str, str], float] = {}

    def add_room(self, name: str, concepts: List[str]):
        self.rooms[name] = set(concepts)

    def find_connections(self, min_overlap: int = 3) -> List[Tuple[str, str, List[str], float]]:
        room_names = list(self.rooms.keys())
        connections = []
        for i, a in enumerate(room_names):
            for b in room_names[i+1:]:
                shared = self.rooms[a] & self.rooms[b]
                if len(shared) >= min_overlap:
                    score = len(shared) / min(len(self.rooms[a]), len(self.rooms[b]), 1)
                    self.edges[(a, b)] = score
                    connections.append((a, b, list(shared), score))
        connections.sort(key=lambda x: x[3], reverse=True)
        return connections

    def get_strongest_path(self, from_room: str, to_room: str) -> List[str]:
        if from_room not in self.rooms or to_room not in self.rooms:
            return []
        # BFS with edge weights
        visited = {from_room}
        queue = [(from_room, [from_room])]
        while queue:
            current, path = queue.pop(0)
            if current == to_room:
                return path
            for (a, b), score in self.edges.items():
                neighbor = b if a == current else (a if b == current else None)
                if neighbor and neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        return []


class CrossPollinator:
    """Main engine — analyzes rooms and finds cross-pollination opportunities."""

    def __init__(self, min_overlap: int = 3, max_concepts: int = 30):
        self.min_overlap = min_overlap
        self.max_concepts = max_concepts
        self.extractor = ConceptExtractor(max_terms=max_concepts)
        self.graph = RoomGraph()

    def analyze(self, room_texts: Dict[str, List[str]]) -> List[Synergy]:
        # Extract concepts per room
        all_docs = []
        for texts in room_texts.values():
            all_docs.extend(texts)
        self.extractor.fit(all_docs)

        for room_name, texts in room_texts.items():
            combined = " ".join(texts)
            concepts = [term for term, score in self.extractor.extract(combined)]
            self.graph.add_room(room_name, concepts)

        # Find connections
        connections = self.graph.find_connections(min_overlap=self.min_overlap)

        synergies = []
        for a, b, shared, score in connections:
            rec = f"Transfer {shared[0]} expertise from {a} to {b}"
            if len(shared) > 1:
                rec = f"Merge {', '.join(shared[:3])} between {a} and {b}"
            synergies.append(Synergy(
                room_a=a, room_b=b,
                shared_concepts=shared[:10],
                overlap_score=round(score, 3),
                recommendation=rec,
            ))
        return synergies


__all__ = ["ConceptExtractor", "RoomGraph", "CrossPollinator", "Synergy"]

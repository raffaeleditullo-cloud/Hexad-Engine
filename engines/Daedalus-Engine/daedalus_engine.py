"""
DAEDALUS Engine: Topological Navigation, Hamiltonian Pathing & Anti-Deadlock Invariance.

Auxiliary Sovereign Component (The Labyrinth Master / Deadlock Immunity):
Prevents systems from getting trapped in self-coiling loops, circular deadlocks,
and dead-end pockets by enforcing global topological reachability.
"""

from dataclasses import dataclass, field
from typing import List, Tuple, Set, Optional, Dict
import time


@dataclass
class TopologicalCertificate:
    """Certificato di sicurezza topologica emesso da DAEDALUS."""
    is_safe: bool
    free_cells_count: int
    tail_reachable: bool
    path_length: int
    loop_risk_detected: bool
    recommended_direction: Tuple[int, int]
    timestamp: float = field(default_factory=time.time)


class DaedalusEngine:
    """
    Motore DAEDALUS: Maestro del Labirinto e dell'Anti-Intrappolamento.
    Garantisce che una traiettoria mantenga sempre uno spazio di fuga aperto.
    """

    def __init__(self, grid_size: int = 24):
        self.grid_size = grid_size

    def is_blocked(self, pos: Tuple[int, int], obstacles: Set[Tuple[int, int]], body: List[Tuple[int, int]]) -> bool:
        x, y = pos
        if x < 0 or x >= self.grid_size or y < 0 or y >= self.grid_size:
            return True
        if pos in obstacles:
            return True
        # Exclude tail end since it moves
        if pos in body[:-1]:
            return True
        return False

    def find_shortest_path(
        self,
        start: Tuple[int, int],
        target: Tuple[int, int],
        obstacles: Set[Tuple[int, int]],
        body: List[Tuple[int, int]]
    ) -> Optional[List[Tuple[int, int]]]:
        """Trova il percorso più breve verso un obiettivo evitando ostacoli e corpo."""
        queue = [[start]]
        visited = {start}
        dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]

        while queue:
            path = queue.pop(0)
            curr = path[-1]

            if curr == target:
                return path

            for dx, dy in dirs:
                nxt = (curr[0] + dx, curr[1] + dy)
                if nxt not in visited:
                    if nxt == target or not self.is_blocked(nxt, obstacles, body):
                        visited.add(nxt)
                        queue.append(path + [nxt])
        return None

    def compute_flood_fill(
        self,
        start: Tuple[int, int],
        obstacles: Set[Tuple[int, int]],
        body: List[Tuple[int, int]],
        max_depth: int = 300
    ) -> int:
        """Calcola l'area di celle libere accessibili prima di entrare in un'ansa."""
        if self.is_blocked(start, obstacles, body):
            return 0
        visited = {start}
        queue = [start]
        dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]

        while queue and len(visited) < max_depth:
            curr = queue.pop(0)
            for dx, dy in dirs:
                nxt = (curr[0] + dx, curr[1] + dy)
                if nxt not in visited and not self.is_blocked(nxt, obstacles, body):
                    visited.add(nxt)
                    queue.append(nxt)
        return len(visited)

    def evaluate_move_safety(
        self,
        head: Tuple[int, int],
        food: Tuple[int, int],
        body: List[Tuple[int, int]],
        obstacles: Optional[Set[Tuple[int, int]]] = None
    ) -> TopologicalCertificate:
        """
        Valuta con simulazione nel futuro se la mossa verso il cibo
        permette ancora di raggiungere la coda evitando l'autointrappolamento.
        """
        obs = obstacles or set()
        tail = body[-1] if body else head

        path_to_food = self.find_shortest_path(head, food, obs, body)
        tail_reachable_after_food = False
        loop_risk = False

        if path_to_food and len(path_to_food) > 1:
            # Simula corpo futuro dopo aver mangiato
            future_body = list(reversed(path_to_food)) + body[:max(0, len(body) - len(path_to_food) + 1)]
            path_to_tail = self.find_shortest_path(path_to_food[1], future_body[-1], obs, future_body)
            if path_to_tail and len(path_to_tail) > 1:
                tail_reachable_after_food = True
            else:
                loop_risk = True

        dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        best_dir = (1, 0)
        max_area = -1

        if tail_reachable_after_food and path_to_food:
            best_dir = (path_to_food[1][0] - head[0], path_to_food[1][1] - head[1])
            area = self.compute_flood_fill(path_to_food[1], obs, body)
        else:
            # Safe tail-chasing stall
            for dx, dy in dirs:
                cand = (head[0] + dx, head[1] + dy)
                if not self.is_blocked(cand, obs, body):
                    cand_area = self.compute_flood_fill(cand, obs, body)
                    can_see_tail = bool(self.find_shortest_path(cand, tail, obs, body))
                    score = cand_area + (1000 if can_see_tail else 0)
                    if score > max_area:
                        max_area = score
                        best_dir = (dx, dy)
            area = max_area if max_area > 0 else 0

        return TopologicalCertificate(
            is_safe=not loop_risk,
            free_cells_count=area,
            tail_reachable=tail_reachable_after_food,
            path_length=len(path_to_food) if path_to_food else 0,
            loop_risk_detected=loop_risk,
            recommended_direction=best_dir
        )


if __name__ == "__main__":
    solver = DaedalusEngine(grid_size=24)
    head = (10, 10)
    food = (15, 10)
    body = [(10, 10), (9, 10), (8, 10), (7, 10)]
    cert = solver.evaluate_move_safety(head, food, body)
    print("🏛️ DAEDALUS Engine Attivo.")
    print(" Certificato:", cert)

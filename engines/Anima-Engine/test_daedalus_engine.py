"""
Test Suite per DAEDALUS Engine: Verifica Navigazione Anti-Trappola e Flood-Fill.
"""

import unittest
from daedalus_engine import DaedalusEngine


class TestDaedalusEngine(unittest.TestCase):
    def setUp(self):
        self.engine = DaedalusEngine(grid_size=24)

    def test_shortest_path_found(self):
        start = (2, 2)
        target = (5, 2)
        body = [(2, 2), (1, 2)]
        path = self.engine.find_shortest_path(start, target, set(), body)
        self.assertIsNotNone(path)
        self.assertEqual(len(path), 4)

    def test_flood_fill_boundary(self):
        area = self.engine.compute_flood_fill((0, 0), set(), [(0, 0)])
        self.assertGreater(area, 50)

    def test_anti_trap_avoidance(self):
        # Serpente quasi a cerchio che rischia di chiudersi
        head = (5, 5)
        food = (5, 6) # Cibo proprio dentro la morsa
        # Il corpo chiude quasi tutto il perimetro
        body = [(5, 5), (6, 5), (6, 6), (6, 7), (5, 7), (4, 7), (4, 6), (4, 5)]
        cert = self.engine.evaluate_move_safety(head, food, body)
        self.assertIsNotNone(cert.recommended_direction)
        # Deve raccomandare una mossa valida che non sia un suicidio immediato
        dx, dy = cert.recommended_direction
        nxt = (head[0] + dx, head[1] + dy)
        self.assertFalse(self.engine.is_blocked(nxt, set(), body))


if __name__ == '__main__':
    unittest.main()

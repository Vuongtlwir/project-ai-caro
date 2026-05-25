from __future__ import annotations

class KillerHeuristic:
    #Lưu trữ nước đi gây ra sự cắt đứt như một nước đi quyết định.
    def store_killer(self, depth, move):
        if depth not in self.killer_moves:
            self.killer_moves[depth] =[]
        killer = self.killer_moves[depth]

        if move in killer:
            return
        
        killer.insert(0, move)
        if len(killer) > self.max_killers_per_depth:
            killer.pop()
from .bfs import BFS
from .bfs_early import BFS_EARLY
from .dfs import DFS
from .dfs_early import DFS_EARLY
from .ids import IDS
from .ids_early import IDS_EARLY
from .ucs import UCS
from .greedy import Greedy
from .A_star import AStar
from .ida_star import IDAStar
from .simplehillclimbing import SimpleHillClimbing
from .steepestascenthillclimbing import SteepestAscentHillClimbing
from .stochastichillclimbing import StochasticHillClimbing
from .randomrestarthillclimbing import RandomRestartHillClimbing
from .localbeamsearch import LocalBeamSearch

ALG_MAP = {
    "BFS": BFS(),
    "BFS Early": BFS_EARLY(),
    "DFS": DFS(),
    "DFS Early": DFS_EARLY(),
    "IDS": IDS(),
    "IDS Early": IDS_EARLY(),
    "UCS": UCS(),
    "Greedy": Greedy(),
    "A*": AStar(),
    "IDA*": IDAStar(),
    "Simple HC": SimpleHillClimbing(),
    "Steepest Ascent HC": SteepestAscentHillClimbing(),
    "Stochastic HC": StochasticHillClimbing(),
    "Random Restart HC": RandomRestartHillClimbing(),
    "Local Beam Search": LocalBeamSearch(),
}
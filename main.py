from sc2 import maps
from sc2.player import Bot, Computer
from sc2.main import run_game
from sc2.data import Race, Difficulty
from Agent import JugadorAgent


if __name__ == "__main__":

    run_game(
            maps.get("BerlingradAIE"), [
                Bot(Race.Terran, JugadorAgent()),
                Computer(Race.Zerg, Difficulty.Medium)
            ],
            realtime=True,
    )

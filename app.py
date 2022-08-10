from rocketry import Rocketry
from loguru import logger

from src.histParser import init_scrapper
from src.modules.misc import getDuration, save_data

app = Rocketry()


def run(data):
    results = init_scrapper(data["endpoint"], data["lookup_class"])
    save_data(results, "b_id", data["endpoint"])


@app.task("every 2 hours")
def main():
    games_endpoint = [{"endpoint":"doubles", "lookup_class":"double-single"},{"endpoint":"crashes", "lookup_class":"crash-single"}]

    for idx, game in enumerate(games_endpoint):
        try:
            run(game)
        except Exception as e:
            logger.error(e)


if __name__ == "__main__":
    try:
        app.run()
    except Exception as e:
        logger.error(e)

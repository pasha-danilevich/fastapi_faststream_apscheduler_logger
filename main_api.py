from api.api import run_api, some_api
from api.routers.some import some_some
from bg.routers.bg_router import some_routers
from bg.services.schedulers import some_service
from bg.services.workers import some_w
from logger import logger


def main():
    logger.info('Start api')
    some_service(11, 11)
    some_w()
    some_routers()
    some_api()
    some_some()

    run_api()


if __name__ == "__main__":
    main()

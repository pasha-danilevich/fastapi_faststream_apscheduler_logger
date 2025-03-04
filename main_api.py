from api.api import run_api, some_api
from api.routers.some import some_some
from bg.api import l
from bg.routers.bg_router import some_routers
from bg.services.schedulers import some_service
from bg.services.workers import some_sql_func
from logger import logger


def main():
    logger.info('Start api')
    a = [x for x in range(1000)]
    some_service(a, 11)

    sql = """select count(*)
    from person
    where 1 = 1
      and name is not null
      and {condition};"""

    some_sql_func(sql)
    some_routers()
    some_api()
    some_some(11, 12)
    l()

    # run_api()


if __name__ == "__main__":
    main()




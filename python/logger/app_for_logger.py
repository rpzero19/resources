# https://stackoverflow.com/questions/40628042/python-creating-a-time-rotating-log-from-a-config-file

# https://stackoverflow.com/questions/25187083/python-logging-to-multiple-handlers-at-different-log-levels

import logging
import logging.config
import logging.handlers
import time


def multiply(num1, num2):  # just multiply two numbers
    log.debug("Executing multiply function.")
    return num1 * num2

def another_error_func(y):
    try:
        log.info("started");
        x = 14
        z = x / y
    except Exception as ex:
        log.exception("Encountered {0} when trying to perform calculation.".format(ex))
    else:
        log.info("ended");
        return x / y * y


# In modules, you can use
# logging.config.fileConfig('helpers/logging.cfg')
# loggerA = logging.getLogger('main.parameters')


if __name__ == '__main__':

    logging.config.fileConfig('logging.cfg')
    log = logging.getLogger("main")

    log.info("start")
    # Log some messages
    multiply(1,3)
    another_error_func(0)
    try:
        for i in range(20):
            log.info('i = %d' % i)
            multiply(1, 3)
            # time.sleep(1)
    except OSError as e:
        log.error(e, exc_info=True)
    except:
        log.error("uncaught exception: %s", traceback.format_exc())




    # while True:
    #     time.sleep(1)
    #     logger.info("log more")
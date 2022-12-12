import time

from acre import Timer, log


MAX_TIMEOUT = 10 * 60


class RetryError(Exception):
    pass


def retry(fnc, count=0, timeout=None, period=1, message="retry"):
    if not timeout:
        timeout = MAX_TIMEOUT
    if timeout > 60 * 16:
        log.warning(f'Timeout is longer than 16 minutes (timeout={timeout}s)')

    if period > 60:
        log.warning(f'The period between consecutive retries is longer than one minute (period={period}s)')

    num_retries = 0
    result = 'unknown'

    log.note(f'testing if "{message}" will succeed '
             f'in next {timeout} seconds. The retry interval is {period} seconds')
    start_time = time.time()
    until_time = start_time + timeout + period  # allow one period to ensure at least two executions
    log.debug(f"retry_until: start: {time.ctime(start_time)}, until: {time.ctime(until_time)}")
    while time.time() < until_time:
        now = time.time()
        next_try_at = time.time() + period
        num_retries += 1
        result = fnc()
        log.note(f'{ordinal(num_retries)} try after {now - start_time:.4f} seconds. result: {result}')
        log.debug(f"next try at: {time.strftime('%H:%M:%S', time.localtime(next_try_at))}")
        if result:
            log.debug(f"{message}. succeeded got '{result}'")
            return result

        if count and num_retries >= count:
            break
        if next_try_at > until_time:
            log.debug(f"next_try_at {next_try_at} > until_time {until_time}. break")
            break
        wait_util_next_try = next_try_at - time.time()

        if wait_util_next_try < 0:
            log.debug("continue to next try with out sleep")
            continue
        log.debug(f"sleeping for {wait_util_next_try:.4f}")
        Timer().wait(seconds=wait_util_next_try,
                     reason=f"retry_until({message}): sleeping for {wait_util_next_try}s")

    raise RetryError(f"{message} failed after {timeout} seconds and {num_retries}/{count} retries")


def ordinal(n):
    return "%d%s" % (n, "tsnrhtdd"[(n / 10 % 10 != 1) * (n % 10 < 4) * n % 10::4])


    

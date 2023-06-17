"""时间mock模块"""
import time

from datetime import datetime
import software_app.service.charge as charge
import software_app.service.schd as schd

FAST_FORWARD_RATE = 60

# __boot_datetime = datetime.now()
__boot_timestamp = round(time.time())


# def reset_time() -> None:
#     global __boot_datetime
#     global __boot_timestamp
#     __boot_datetime = datetime.now()
#     __boot_timestamp = round(time.time())
test_today = datetime.now().date().strftime("%Y-%m-%d")
test_begin_time = datetime.strptime(test_today+" 00:40:00", "%Y-%m-%d %H:%M:%S")
__boot_datetime = test_begin_time

def check_time(mocked_datetime):
    print("[check]", mocked_datetime)
    str = mocked_datetime.strftime("%Y-%m-%d %H:%M:%S")
    str = str.split(" ")[1]
    str = str.split(":")[1]
    if(str == "00" or str == "30"):
        print("[check]", mocked_datetime)
        req_list = schd.scheduler.test_snapshot()
        for req in req_list:
            print("[check]", req.username)
            real_amount = schd.scheduler.calc_real_amount(req, end_time=mocked_datetime)
            # total_cost_sofar,charging_cost_sofar, service_cost = charge.calc_cost(begin_time=req.begin_time, end_time=mocked_datetime, amount=real_amount)
            charge.calc_cost(begin_time=req.begin_time, end_time=mocked_datetime, amount=real_amount)
            # print("[check]", req.username, real_amount, total_cost_sofar,charging_cost_sofar, service_cost)
        time.sleep(2)



def get_timestamp_now() -> int:
    real_timestamp = round(time.time())
    delta = real_timestamp - __boot_timestamp
    mocked_timestamp = __boot_timestamp + delta * FAST_FORWARD_RATE
    return mocked_timestamp


def get_datetime_now() -> datetime:
    real_datetime = datetime.now()
    delta = real_datetime - __boot_datetime
    mocked_datetime = __boot_datetime + delta * FAST_FORWARD_RATE
    return mocked_datetime


if __name__=="__main__":
    while(True):
        time.sleep(2)
        check_time(get_datetime_now())

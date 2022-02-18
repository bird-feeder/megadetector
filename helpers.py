import datetime
import os
import sys

import GPUtil


def crude_walltime_limit():
    TOTAL_NUM_OF_IMGS = int(os.environ['TOTAL_NUM_OF_IMGS'])
    wt = str(datetime.timedelta(seconds=TOTAL_NUM_OF_IMGS))[:-3]
    if wt[1] == ':':
        wt = f'0{wt}'
    return wt


def get_avail_gpus():
    avail_gpus = GPUtil.getAvailable(order='load',
                                     limit=1,
                                     maxLoad=0.5,
                                     maxMemory=0.5,
                                     includeNan=False,
                                     excludeID=[],
                                     excludeUUID=[])
    use_gpus = ','.join([str(x) for x in avail_gpus])
    return use_gpus


if __name__ == '__main__':
    if '--time' in sys.argv:
        print(crude_walltime_limit())
    elif '--gpus' in sys.argv:
        print(get_avail_gpus())

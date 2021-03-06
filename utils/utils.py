import json
import os
import time


class ArgDict(dict):
    def __init__(self, *args, **kwargs):
        super(ArgDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


class AverageMeter(object):
    """Computes and stores the average and current value."""

    def __init__(self):
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count


class Timer(object):
    """Computes elasped time."""

    def __init__(self):
        self.reset()

    def reset(self):
        self.running = True
        self.total = 0
        self.start = time.time()
        return self

    def resume(self):
        if not self.running:
            self.running = True
            self.start = time.time()
        return self

    def stop(self):
        if self.running:
            self.running = False
            self.total += time.time() - self.start
        return self

    def time(self):
        if self.running:
            return self.total + time.time() - self.start
        return self.total


def dump_log(config, metrics, split):
    log_path = os.path.join(config.result_dir, config.run_name, 'logs.json')
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    result = {}
    if os.path.isfile(log_path):
        with open(log_path) as fp:
            result = json.load(fp)
    if split in result:
        result[split].append(metrics)
    else:
        result[split] = [metrics]
    with open(log_path, 'w') as fp:
        json.dump(result, fp)

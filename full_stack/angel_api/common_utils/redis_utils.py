import json

import redis

from common_utils.log_utils import LogUtils


class RedisHelper:

    def __init__(self):
        self.logger_obj = LogUtils.return_logger(__name__)
        self.rds_clnt = redis.Redis()
        self.logger_obj.info('Redis Client Initiated : {}'.format(self.rds_clnt))

    def set_json(self, k, val_list_or_dict):
        op = self.rds_clnt.set(k, json.dumps(val_list_or_dict))
        self.logger_obj.debug(op)

    def get_json(self, k, dflt=None):
        op = self.rds_clnt.get(k)
        self.logger_obj.debug(op)
        return json.loads(op) if op else dflt


from enum import Enum
from pydantic import BaseModel, ConfigDict, model_validator

FLOW_LOG_VERSION = 2

class Action(str, Enum):
    ACCEPT = 'ACCEPT'
    REJECT = 'REJECT'


class LogStatus(str, Enum):
    OK = 'OK'
    NODATA = 'NODATA'
    SKIPDATA = 'SKIPDATA'


class FlowLogRecord(BaseModel):

    model_config = ConfigDict(str_strip_whitespace=True)

    version: int
    account_id: str
    interface_id: str
    srcaddr: str
    dstaddr: str
    scrport: int
    dstport: int
    protocol: int
    packets: int
    bytes: int
    start: int
    end: int
    action: Action
    log_status: LogStatus

    @model_validator(mode='after')
    def check_version(self):
        version = self.version
        if FLOW_LOG_VERSION != version:
            raise ValueError(f'Unexpected flow log version : {version}, expected: {FLOW_LOG_VERSION}')
        return self
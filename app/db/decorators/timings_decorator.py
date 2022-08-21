import datetime
from typing import List

from sqlalchemy import TypeDecorator, String


class TimingsDecorator(TypeDecorator):
    impl = String

    def __init__(self, length=None, **kwargs):
        super().__init__(length, **kwargs)

    def process_literal_param(self, timings, dialect) -> str:
        """
        Converts pydantic values to db acceptable

        :param timings:
        :param dialect:
        :return:
        """
        return ",".join([str(x.total_seconds()) for x in timings])

    process_bind_param = process_literal_param

    def process_result_value(self, value, dialect) -> List[datetime.timedelta]:
        return [datetime.timedelta(float(x) / (24 * 60 * 60)) for x in value.split(',')]

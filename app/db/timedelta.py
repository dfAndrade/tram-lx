import re
from datetime import timedelta, datetime

from sqlalchemy import TypeDecorator, cast, Interval


class TimeDelta(TypeDecorator):
    impl = Interval

    def bind_expression(self, bindvalue):
        return cast(bindvalue, self)

    def result_processor(self, dialect, coltype):
        super_rp = super(TimeDelta, self).result_processor(dialect, coltype)

        def handle_raw_string(value):
            t = datetime.strptime(value, "%H:%M:%S")
            delta = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
            return delta

        def process(value):
            if value is None:
                return None

            return super_rp(handle_raw_string(value))

        return process

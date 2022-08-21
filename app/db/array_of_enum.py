import re

from sqlalchemy import TypeDecorator, cast, String
from sqlalchemy.dialects.postgresql import ARRAY


class ArrayOfEnum(TypeDecorator):
    impl = ARRAY

    def bind_expression(self, bindvalue):
        return cast(bindvalue, String)

    def process_literal_param(self, value, dialect):
        super(ArrayOfEnum, self).process_literal_param(value, dialect)

    def bind_processor(self, dialect):
        return super().bind_processor(dialect)

    def result_processor(self, dialect, coltype):
        super_rp = super(ArrayOfEnum, self).result_processor(dialect, coltype)

        def handle_raw_string(value):
            """ Reads raw string from **DB**"""
            inner = re.match(r"^(.*)$", value).group(1)

            return inner.split(",") if inner else []

        def process(value):
            if value is None:
                return None

            return super_rp(handle_raw_string(value))

        return process

from typing import List

from sqlalchemy import TypeDecorator, String

from app.db.models import Line


class LineDecorator(TypeDecorator):
    impl = String

    def __init__(self, length=None, **kwargs):
        super().__init__(length, **kwargs)

    def process_literal_param(self, lines, dialect) -> str:
        """
        Converts pydantic value to db acceptable<br>

        Note: Lines are converted to their string names

        :param lines:
        :param dialect:
        :return:
        """
        return lines

    process_bind_param = process_literal_param

    def process_result_value(self, value, dialect) -> List[Line]:
        return [Line[x] for x in value.split(',')]

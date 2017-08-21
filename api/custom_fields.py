from flask_restful import fields


class DateTimeIsoZ(fields.DateTime):
    def __init__(self, dt_format='iso8601', **kwargs):
        super(fields.DateTime, self).__init__(**kwargs)
        self.dt_format = dt_format

    def format(self, dt):
        return str(dt.isoformat()) + "Z"

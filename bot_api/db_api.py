import datetime
from app import db, app
from database import BotRequest as DbBotRequest

DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"


class BotRequest(object):
    """
    BotRequest model interface class
    """

    def __init__(self, resp):
        self.text = resp.text
        from_user = resp.from_user
        self.user_id = from_user.id
        self.user_name = from_user.username
        self.first_name = from_user.first_name
        self.last_name = from_user.last_name
        self.date = resp.date

    def to_dict(self):
        """
        returns interface dict
        :return:
        """
        return {
            'text': self.text,
            'user_id': self.user_id,
            'user_name': self.user_name,
            'date': self.date,
            'first_name': self.first_name,
            'last_name': self.last_name
        }

    def __repr__(self):
        return '<BotRequest: username %s (%s)>' % (
            self.user_name, self.user_id
        )

    def db_save(self):
        """
        Saves Bot request to the Db
        :return:
        """
        request = DbBotRequest(**self.to_dict())
        db.session.add(request)
        db.session.commit()

    @staticmethod
    def get_history(user_id):
        """
        Gets history of the Bot requests
        :param user_id:
        :return:
        """
        requests = DbBotRequest.query.filter_by(
            user_id=user_id
        )
        return '\n'.join(['%s\t%s' % (
            request.text,
            datetime.datetime.strftime(request.time, DATE_TIME_FORMAT))
                          for request in requests])

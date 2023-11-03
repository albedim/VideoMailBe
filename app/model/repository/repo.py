from app.configuration.config import sql


class Repository:

    @classmethod
    def commit(cls):
        try:
            sql.commit()
        except Exception as exc:
            sql.rollback()
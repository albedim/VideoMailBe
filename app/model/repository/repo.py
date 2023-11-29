from app.configuration.config import sql


class Repository:

    @classmethod
    def commit(cls):
        try:
            sql.session.commit()
        except Exception as exc:
            sql.session.rollback()

    @classmethod
    def endTransactions(cls):
        sql.session.close()
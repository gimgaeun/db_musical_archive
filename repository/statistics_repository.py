import pandas as pd


class StatisticsRepository:
    def __init__(self, con):
        self._con = con

    def total_view_count(self):

        query = """
        SELECT COUNT(*)
        FROM Record
        """

        return self._con.execute(query).fetchone()[0]

    def total_spent(self):

        query = """
        SELECT SUM(ticket_price)
        FROM Record
        """

        return self._con.execute(query).fetchone()[0]

    def performance_ranking(self):

        query = """
        SELECT
            p.title,
            COUNT(*) AS view_count

        FROM Record r

        JOIN Performance p
            ON r.performance_id = p.performance_id

        GROUP BY p.title

        ORDER BY view_count DESC
        """

        return self._con.execute(query).df()

    def actor_ranking(self):

        query = """
        SELECT
            r.cast_name,
            COUNT(*) AS view_count

        FROM Record r

        GROUP BY r.cast_name

        ORDER BY view_count DESC
        """

        return self._con.execute(query).df()

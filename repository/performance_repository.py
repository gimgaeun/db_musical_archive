import duckdb
import pandas as pd


class PerformanceRepository:
    # 생성자
    # DuckDB 연결 객체 저장
    def __init__(self, con: duckdb.DuckDBPyConnection):
        self._con = con

    # 전체 공연 목록 조회
    def find_all(self) -> pd.DataFrame:

        query = """
        SELECT *
        FROM Performance
        ORDER BY title
        """

        # 공연 정보를 DataFrame 형태로 반환
        return self._con.execute(query).df()

    # 공연 ID로 공연 조회
    def find_by_id(self, performance_id: int) -> pd.DataFrame:

        query = """
        SELECT *
        FROM Performance
        WHERE performance_id = ?
        """

        # 특정 공연 조회
        return self._con.execute(query, [performance_id]).df()

    # 공연명 검색
    def find_by_title(self, keyword: str) -> pd.DataFrame:

        query = """
        SELECT *
        FROM Performance
        WHERE title LIKE ?
        """

        # 부분 문자열 검색 수행
        return self._con.execute(query, [f"%{keyword}%"]).df()

    # 공연 상세 정보 조회
    def find_detail(self, performance_id: int) -> pd.DataFrame:

        query = """
        SELECT
            p.performance_id,
            p.title,
            p.start_date,
            p.end_date,
            p.running_time,
            p.age_limit,
            p.poster_url,

            t.theater_name,
            t.location,

            a.actor_name,
            c.role_name

        FROM Performance p

        JOIN Theater t
            ON p.theater_id = t.theater_id

        JOIN Casting c
            ON p.performance_id = c.performance_id

        JOIN Actor a
            ON c.actor_id = a.actor_id

        WHERE p.performance_id = ?
        """

        # 공연 상세 정보 반환
        # 공연 정보 + 공연장 정보 + 출연 배우 정보
        return self._con.execute(query, [performance_id]).df()

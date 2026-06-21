import duckdb
import pandas as pd


class ActorRepository:
    # 생성자
    # DuckDB 연결 객체 저장
    def __init__(
        self,
        con,
    ):
        self._con = con

    # 전체 배우 목록 조회
    def find_all(self):

        query = """
        SELECT *
        FROM Actor
        ORDER BY actor_name
        """

        # 배우 이름 기준 오름차순 정렬
        return self._con.execute(query).df()

    # 배우 이름 검색
    def find_by_name(
        self,
        keyword,
    ):

        query = """
        SELECT *
        FROM Actor
        WHERE actor_name LIKE ?
        """

        # 부분 문자열 검색 수행
        return self._con.execute(query, [f"%{keyword}%"]).df()

    # 배우 상세 정보 조회
    def find_detail(
        self,
        actor_id,
    ):

        query = """
        SELECT

            a.actor_id,
            a.actor_name,
            a.birth_date,
            a.profile_image,
            a.agency,

            p.title,
            c.role_name

        FROM Actor a

        JOIN Casting c
            ON a.actor_id = c.actor_id

        JOIN Performance p
            ON c.performance_id = p.performance_id

        WHERE a.actor_id = ?
        """

        # 배우 기본 정보
        # 출연 공연
        # 배역 정보 조회
        return self._con.execute(query, [actor_id]).df()

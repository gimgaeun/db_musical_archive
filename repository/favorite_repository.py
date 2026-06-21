import pandas as pd


class FavoriteRepository:
    # 생성자
    # DuckDB 연결 객체 저장
    def __init__(
        self,
        con,
    ):

        self._con = con

    # 관심 공연 추가
    def add(
        self,
        user_id: int,
        performance_id: int,
    ):

        query = """
        INSERT INTO Favorite
        VALUES (?, ?)
        """

        # 사용자와 공연 정보를 Favorite 테이블에 저장
        self._con.execute(
            query,
            [
                user_id,
                performance_id,
            ],
        )

    # 관심 공연 삭제
    def delete(
        self,
        user_id: int,
        performance_id: int,
    ):

        query = """
        DELETE FROM Favorite
        WHERE user_id = ?
        AND performance_id = ?
        """

        # 특정 관심 공연 삭제
        self._con.execute(
            query,
            [
                user_id,
                performance_id,
            ],
        )

    # 관심 공연 목록 조회
    def find_all(
        self,
        user_id: int,
    ) -> pd.DataFrame:

        query = """
        SELECT

            p.performance_id,
            p.title,
            p.start_date,
            p.end_date,

            t.theater_name

        FROM Favorite f

        JOIN Performance p
            ON f.performance_id = p.performance_id

        JOIN Theater t
            ON p.theater_id = t.theater_id

        WHERE f.user_id = ?

        ORDER BY p.title
        """

        # 관심 공연 목록 반환
        return self._con.execute(query, [user_id]).df()

    # 관심 공연 등록 여부 확인
    def exists(
        self,
        user_id: int,
        performance_id: int,
    ) -> bool:

        query = """
        SELECT COUNT(*)
        FROM Favorite
        WHERE user_id = ?
        AND performance_id = ?
        """

        count = self._con.execute(
            query,
            [
                user_id,
                performance_id,
            ],
        ).fetchone()[0]

        # 1개 이상 존재하면 True
        return count > 0

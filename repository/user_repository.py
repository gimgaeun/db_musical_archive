import duckdb
import pandas as pd


class UserRepository:
    # 생성자
    # DuckDB 연결 객체를 저장
    def __init__(
        self,
        con: duckdb.DuckDBPyConnection,
    ):
        self._con = con

    # 현재 저장된 사용자 수 조회
    def count(self) -> int:

        query = """
        SELECT COUNT(*)
        FROM Users
        """

        # COUNT 결과는 한 개의 값만 반환되므로 fetchone 사용
        return self._con.execute(query).fetchone()[0]

    # 사용자 정보 저장
    def save(
        self,
        user_id: int,
        email: str,
        password: str,
        nickname: str,
        join_date: str,
    ):

        query = """
        INSERT INTO Users
        VALUES (?, ?, ?, ?, ?)
        """

        # 사용자 정보 DB 저장
        self._con.execute(
            query,
            [
                user_id,
                email,
                password,
                nickname,
                join_date,
            ],
        )

    # 이메일 중복 검사
    def find_by_email(
        self,
        email: str,
    ) -> pd.DataFrame:

        query = """
        SELECT *
        FROM Users
        WHERE email = ?
        """

        # 조회 결과를 DataFrame 형태로 반환
        return self._con.execute(
            query,
            [email],
        ).df()

    # 로그인 인증
    def login(
        self,
        email: str,
        password: str,
    ) -> pd.DataFrame:

        query = """
        SELECT *
        FROM Users
        WHERE email = ?
        AND password = ?
        """

        # 이메일과 비밀번호가 모두 일치하는 사용자 조회
        return self._con.execute(
            query,
            [
                email,
                password,
            ],
        ).df()

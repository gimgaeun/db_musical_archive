import pandas as pd


class RecordRepository:
    # 생성자
    # DuckDB 연결 객체 저장
    def __init__(
        self,
        con,
    ):

        self._con = con

    # 전체 관람 기록 조회
    def find_all(self) -> pd.DataFrame:

        query = """
        SELECT *
        FROM Record
        ORDER BY view_date DESC
        """

        # 최신 관람일 순 정렬
        return self._con.execute(query).df()

    # 특정 사용자의 관람 기록 조회
    def find_by_user(
        self,
        user_id: int,
    ) -> pd.DataFrame:

        query = """
        SELECT *
        FROM Record
        WHERE user_id = ?
        ORDER BY view_date DESC
        """

        return self._con.execute(
            query,
            [user_id],
        ).df()

    # 관람 기록 저장
    def save(
        self,
        user_id,
        performance_id,
        view_date,
        ticket_price,
        seat_info,
        cast_name,
        score,
        review,
    ):

        # 새로운 관람 기록 번호 생성
        new_id = self.count() + 1

        query = """
        INSERT INTO Record (
            record_id,
            user_id,
            performance_id,
            view_date,
            ticket_price,
            seat_info,
            cast_name,
            score,
            review
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        # 관람 기록 저장
        self._con.execute(
            query,
            [
                new_id,
                user_id,
                performance_id,
                view_date,
                ticket_price,
                seat_info,
                cast_name,
                score,
                review,
            ],
        )

    # 전체 관람 기록 수 조회
    def count(self):

        query = """
        SELECT COUNT(*)
        FROM Record
        """

        return self._con.execute(query).fetchone()[0]

    # 관람 기록 삭제
    def delete(
        self,
        record_id,
    ):

        query = """
        DELETE
        FROM Record
        WHERE record_id = ?
        """

        self._con.execute(
            query,
            [record_id],
        )

    # 관람 기록 상세 조회
    def find_by_id(
        self,
        record_id: int,
    ) -> pd.DataFrame:

        query = """
        SELECT *
        FROM Record
        WHERE record_id = ?
        """

        return self._con.execute(
            query,
            [record_id],
        ).df()

    # 관람 기록 수정
    def update(
        self,
        record_id,
        view_date,
        ticket_price,
        seat_info,
        cast_name,
        score,
        review,
    ):

        query = """
        UPDATE Record
        SET
            view_date = ?,
            ticket_price = ?,
            seat_info = ?,
            cast_name = ?,
            score = ?,
            review = ?
        WHERE record_id = ?
        """

        self._con.execute(
            query,
            [
                view_date,
                ticket_price,
                seat_info,
                cast_name,
                score,
                review,
                record_id,
            ],
        )

    # 공연 정보와 함께 관람 기록 조회
    def find_all_with_performance(self):

        query = """
        SELECT

            r.record_id,
            r.view_date,
            r.score,

            p.performance_id,
            p.title,
            p.poster_url

        FROM Record r

        JOIN Performance p
            ON r.performance_id = p.performance_id

        ORDER BY r.view_date DESC
        """

        return self._con.execute(query).df()

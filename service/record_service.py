class RecordService:
    # 생성자
    # RecordRepository 객체를 전달받아 저장
    def __init__(
        self,
        record_repository,
    ):

        self.record_repository = record_repository

    # 전체 관람 기록 조회
    def get_all_records(
        self,
    ):

        # 공연 정보가 포함된 관람 기록 목록 반환
        return self.record_repository.find_all_with_performance()

    # 특정 관람 기록 조회
    def get_record(
        self,
        record_id,
    ):

        # 관람 기록 번호를 이용하여 조회
        return self.record_repository.find_by_id(record_id)

    # 관람 기록 저장
    def save_record(
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

        # Repository에 저장 요청
        self.record_repository.save(
            user_id,
            performance_id,
            view_date,
            ticket_price,
            seat_info,
            cast_name,
            score,
            review,
        )

    # 관람 기록 삭제
    def delete_record(
        self,
        record_id,
    ):

        # 특정 관람 기록 삭제
        self.record_repository.delete(record_id)

    # 관람 기록 수정
    def update_record(
        self,
        record_id,
        view_date,
        ticket_price,
        seat_info,
        cast_name,
        score,
        review,
    ):

        # 기존 관람 기록 수정
        self.record_repository.update(
            record_id,
            view_date,
            ticket_price,
            seat_info,
            cast_name,
            score,
            review,
        )

class PerformanceService:
    # 생성자
    # PerformanceRepository 객체를 전달받아 저장
    def __init__(
        self,
        performance_repository,
    ):

        self.performance_repository = performance_repository

    # 전체 공연 목록 조회
    def get_all_performances(
        self,
    ):

        # Repository에 전체 공연 조회 요청
        return self.performance_repository.find_all()

    # 공연명 검색
    def search_performance(
        self,
        keyword,
    ):

        # 공연명을 기준으로 검색 수행
        return self.performance_repository.find_by_title(keyword)

    # 공연 ID로 공연 조회
    def get_performance(
        self,
        performance_id,
    ):

        # 특정 공연 정보 조회
        return self.performance_repository.find_by_id(performance_id)

    # 공연 상세 정보 조회
    def get_performance_detail(
        self,
        performance_id,
    ):

        # 공연 정보
        # 공연장 정보
        # 출연 배우 및 배역 정보 조회
        return self.performance_repository.find_detail(performance_id)

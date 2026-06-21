class ActorService:
    # 생성자
    # ActorRepository 객체를 전달받아 저장
    def __init__(
        self,
        actor_repository,
    ):

        self.actor_repository = actor_repository

    # 전체 배우 목록 조회
    def get_all_actors(
        self,
    ):

        # Repository에 전체 배우 조회 요청
        return self.actor_repository.find_all()

    # 배우 이름 검색
    def search_actor(
        self,
        keyword,
    ):

        # 배우 이름을 기준으로 검색 수행
        return self.actor_repository.find_by_name(keyword)

    # 배우 상세 정보 조회
    def get_actor_detail(
        self,
        actor_id,
    ):

        # 배우 기본 정보
        # 출연 작품
        # 배역 정보 조회
        return self.actor_repository.find_detail(actor_id)

class FavoriteService:
    # 생성자
    # FavoriteRepository 객체를 전달받아 저장
    def __init__(
        self,
        favorite_repository,
    ):

        self.favorite_repository = favorite_repository

    # 관심 공연 등록
    def add_favorite(
        self,
        user_id,
        performance_id,
    ):

        # 이미 등록된 공연인지 확인
        if self.favorite_repository.exists(
            user_id,
            performance_id,
        ):
            print("이미 등록된 관심 공연입니다.")

            return

        # 관심 공연 저장
        self.favorite_repository.add(
            user_id,
            performance_id,
        )

        print("관심 공연 등록 완료")

    # 관심 공연 삭제
    def remove_favorite(
        self,
        user_id,
        performance_id,
    ):

        # Favorite 테이블에서 삭제
        self.favorite_repository.delete(
            user_id,
            performance_id,
        )

    # 관심 공연 목록 조회
    def get_favorites(
        self,
        user_id,
    ):

        # 특정 사용자의 관심 공연 조회
        return self.favorite_repository.find_all(user_id)

from datetime import date


class UserService:
    # 생성자
    # UserRepository 객체를 전달받아 저장
    def __init__(self, user_repository):
        self.user_repository = user_repository

    # 회원가입 기능
    def signup(self, email, password, nickname):

        # 입력한 이메일이 이미 존재하는지 조회
        exists = self.user_repository.find_by_email(email)

        # 조회 결과가 존재하면 회원가입 실패
        if not exists.empty:
            print("이미 사용중인 이메일입니다.")
            return False

        # 새로운 사용자 번호 생성
        # 현재 저장된 사용자 수 + 1
        user_id = self.user_repository.count() + 1

        # User 테이블에 사용자 정보 저장
        self.user_repository.save(
            user_id,  # 사용자 번호
            email,  # 이메일
            password,  # 비밀번호
            nickname,  # 닉네임
            str(date.today()),  # 가입일
        )

        print("회원가입 성공")
        return True

    # 로그인 기능
    def login(self, email, password):

        # 이메일과 비밀번호가 일치하는 사용자 조회
        result = self.user_repository.login(email, password)

        # 조회 결과가 존재하면 True 반환
        # 존재하지 않으면 False 반환
        return not result.empty

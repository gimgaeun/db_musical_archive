from views.main_view import MainView
from views.actor_view import ActorView


class ViewRouter:
    # 정적 메서드
    # 화면 전환을 담당하는 공통 라우터
    @staticmethod
    def navigate(
        page,
        con,
        index,
    ):

        # 현재 화면의 모든 컨트롤 제거
        page.controls.clear()

        # ==========================
        # 홈 화면 이동
        # ==========================
        if index == 0:
            page.add(MainView(con).build(page))

        # ==========================
        # 배우 화면 이동
        # ==========================
        elif index == 1:
            page.add(ActorView(con).build(page))

        # 화면 갱신
        page.update()

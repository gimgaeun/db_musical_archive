import flet as ft

from repository.actor_repository import ActorRepository
from service.actor_service import ActorService

from components.navigation import AppNavigation
from views.actor_detail_view import ActorDetailView


class ActorView:
    # 생성자
    # 배우 목록 화면 초기화
    def __init__(self, con):

        # DuckDB 연결 객체 저장
        self.con = con

        # 배우 관련 서비스 객체 생성
        self.actor_service = ActorService(ActorRepository(con))

    # 네비게이션 메뉴 이동 처리
    def change_page(
        self,
        page,
        index,
    ):

        # 기존 화면 제거
        page.controls.clear()

        # 홈 화면 이동
        if index == 0:
            from views.main_view import MainView

            page.add(MainView(self.con).build(page))

        # 배우 목록 화면 이동
        elif index == 1:
            page.add(ActorView(self.con).build(page))

        # 관람 기록 화면 이동
        elif index == 2:
            from views.record_view import RecordView

            page.add(RecordView(self.con).build(page))

        # 화면 갱신
        page.update()

    # 배우 목록 화면 생성
    def build(
        self,
        page,
    ):

        # 전체 배우 목록 조회
        actor_df = self.actor_service.get_all_actors()

        cards = []

        # 배우 수만큼 카드 생성
        for _, row in actor_df.iterrows():
            card = ft.Container(
                # 배우 클릭 시 상세 화면 이동
                on_click=lambda e, aid=row["actor_id"]: self.open_actor_detail(
                    page,
                    aid,
                ),
                width=220,
                bgcolor="#111827",
                border_radius=12,
                padding=10,
                content=ft.Column(
                    spacing=8,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        # =====================
                        # 배우 프로필 이미지
                        # =====================
                        ft.Container(
                            width=180,
                            height=250,
                            bgcolor="#1E293B",
                            border_radius=8,
                            content=(
                                # 이미지가 존재하는 경우
                                ft.Image(
                                    src=row["profile_image"],
                                    width=180,
                                    height=250,
                                )
                                if row["profile_image"]
                                # 이미지가 없는 경우
                                else ft.Column(
                                    expand=True,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    controls=[
                                        ft.Text(
                                            "🎭",
                                            size=60,
                                        )
                                    ],
                                )
                            ),
                        ),
                        # 배우 이름
                        ft.Text(
                            row["actor_name"],
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color="white",
                        ),
                        # 배우 유형 표시
                        ft.Text(
                            "뮤지컬 배우",
                            size=11,
                            color="#94A3B8",
                        ),
                    ],
                ),
            )

            cards.append(card)

        # 좌측 네비게이션 메뉴 생성
        navigation = AppNavigation.build(
            selected_index=1,
            on_change=lambda e: self.change_page(
                page,
                e.control.selected_index,
            ),
        )

        # 메인 컨텐츠 영역
        content = ft.Container(
            expand=True,
            padding=20,
            content=ft.Column(
                spacing=20,
                controls=[
                    # =====================
                    # 배우 검색창
                    # =====================
                    ft.Container(
                        width=320,
                        bgcolor="#111827",
                        border_radius=12,
                        padding=8,
                        content=ft.TextField(
                            hint_text="🔍 배우 검색",
                            border_color="transparent",
                            bgcolor="#111827",
                            color="white",
                        ),
                    ),
                    # =====================
                    # 배우 카드 목록
                    # =====================
                    ft.Row(
                        spacing=20,
                        controls=cards,
                    ),
                ],
            ),
        )

        # 전체 화면 반환
        return ft.Row(
            expand=True,
            spacing=0,
            controls=[
                navigation,
                content,
            ],
        )

    # 배우 상세 화면 이동
    def open_actor_detail(
        self,
        page,
        actor_id,
    ):

        # 현재 화면 제거
        page.controls.clear()

        # 배우 상세 화면 추가
        page.add(
            ActorDetailView(
                self.con,
                actor_id,
            ).build(page)
        )

        # 화면 갱신
        page.update()

import flet as ft

from repository.performance_repository import PerformanceRepository
from service.performance_service import PerformanceService

from components.navigation import AppNavigation
from views.performance_detail_view import PerformanceDetailView


class MainView:
    # 생성자
    # 메인 화면 초기화
    def __init__(self, con):

        # DuckDB 연결 객체 저장
        self.con = con

        # 공연 관련 서비스 객체 생성
        self.performance_service = PerformanceService(PerformanceRepository(con))

    # 네비게이션 메뉴 이동 처리
    def change_page(
        self,
        page,
        index,
    ):

        # 현재 화면 제거
        page.controls.clear()

        # 홈 화면 이동
        if index == 0:
            page.add(MainView(self.con).build(page))

        # 배우 화면 이동
        elif index == 1:
            from views.actor_view import ActorView

            page.add(ActorView(self.con).build(page))

        # 화면 갱신
        page.update()

    # 공연 상세 화면 이동
    def open_detail(
        self,
        page,
        performance_id,
    ):

        # 현재 화면 제거
        page.controls.clear()

        # 공연 상세 화면 추가
        page.add(
            PerformanceDetailView(
                self.con,
                performance_id,
            ).build(page)
        )

        # 화면 갱신
        page.update()

    # 메인 화면 생성
    def build(
        self,
        page: ft.Page,
    ):

        # 전체 공연 목록 조회
        performance_df = self.performance_service.get_all_performances()

        cards = []

        # 공연 수만큼 카드 생성
        for _, row in performance_df.iterrows():
            # 공연 기간 포맷 변경
            start_date = row["start_date"].strftime("%Y.%m.%d")

            end_date = row["end_date"].strftime("%Y.%m.%d")

            # 공연 카드 생성
            card = ft.Container(
                # 공연 클릭 시 상세 화면 이동
                on_click=lambda e, pid=row["performance_id"]: self.open_detail(
                    page,
                    pid,
                ),
                width=220,
                bgcolor="#111827",
                border_radius=8,
                padding=10,
                content=ft.Column(
                    spacing=8,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        # 공연 포스터 이미지
                        ft.Image(
                            src=row["poster_url"],
                            width=180,
                            height=250,
                        ),
                        # 공연 제목
                        ft.Text(
                            row["title"],
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color="white",
                        ),
                        # 공연 기간
                        ft.Text(
                            f"{start_date} ~ {end_date}",
                            size=11,
                            color="#94A3B8",
                        ),
                    ],
                ),
            )

            cards.append(card)

        # 공통 네비게이션 생성
        navigation = AppNavigation.build(
            selected_index=0,
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
                    # ====================
                    # 공연 검색창
                    # ====================
                    ft.Container(
                        width=320,
                        bgcolor="#111827",
                        border_radius=12,
                        padding=8,
                        content=ft.TextField(
                            hint_text="🔍 공연 검색",
                            border_color="transparent",
                            bgcolor="#111827",
                            color="white",
                        ),
                    ),
                    # ====================
                    # 공연 카드 목록
                    # ====================
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

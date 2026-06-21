import flet as ft

from repository.record_repository import RecordRepository
from service.record_service import RecordService

from components.navigation import AppNavigation


class RecordView:
    # 생성자
    # 관람 기록 목록 화면 초기화
    def __init__(self, con):

        # DuckDB 연결 객체 저장
        self.con = con

        # 관람 기록 서비스 객체 생성
        self.record_service = RecordService(RecordRepository(con))

        # 디버깅용 출력
        print("RECORD VIEW LOADED")

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
            from views.main_view import MainView

            page.add(MainView(self.con).build(page))

        # 배우 화면 이동
        elif index == 1:
            from views.actor_view import ActorView

            page.add(ActorView(self.con).build(page))

        # 관람 기록 화면 이동
        elif index == 2:
            page.add(RecordView(self.con).build(page))

        # 화면 갱신
        page.update()

    # 관람 기록 목록 화면 생성
    def build(
        self,
        page,
    ):

        # 관람 기록 + 공연 정보 조회
        record_df = self.record_service.get_all_records()

        cards = []

        # 관람 기록 수만큼 카드 생성
        for _, row in record_df.iterrows():
            # 평점을 별 모양으로 변환
            stars = "★" * int(row["score"] if row["score"] is not None else 0)

            card = ft.Container(
                width=220,
                bgcolor="#111827",
                border_radius=12,
                padding=10,
                content=ft.Column(
                    spacing=8,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        # 공연 포스터 출력
                        ft.Image(
                            src=row["poster_url"],
                            width=180,
                            height=250,
                        ),
                        # 공연 제목 출력
                        ft.Text(
                            row["title"],
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color="white",
                        ),
                        # 관람일 출력
                        ft.Text(
                            row["view_date"].strftime("%Y.%m.%d"),
                            size=11,
                            color="#94A3B8",
                        ),
                        # 평점 출력
                        ft.Text(
                            stars,
                            color="#FACC15",
                            size=16,
                        ),
                    ],
                ),
            )

            cards.append(card)

        # 공통 네비게이션 생성
        navigation = AppNavigation.build(
            selected_index=2,
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
                    # 관람 기록 검색창
                    # ====================
                    ft.Container(
                        width=320,
                        bgcolor="#111827",
                        border_radius=12,
                        padding=8,
                        content=ft.TextField(
                            hint_text="🔍 관람기록 검색",
                            border_color="transparent",
                            bgcolor="#111827",
                            color="white",
                        ),
                    ),
                    # ====================
                    # 관람 기록 카드 목록
                    # ====================
                    ft.Row(
                        wrap=True,
                        spacing=20,
                        run_spacing=20,
                        controls=cards,
                    ),
                    # 남은 공간 채우기
                    ft.Container(expand=True),
                ],
            ),
        )

        # 관람 기록 추가 버튼(FAB)
        fab = ft.FloatingActionButton(
            # + 아이콘
            icon=ft.Icons.ADD,
        )

        # 전체 화면 반환
        return ft.Stack(
            expand=True,
            controls=[
                # 기본 화면
                ft.Row(
                    expand=True,
                    spacing=0,
                    controls=[
                        navigation,
                        content,
                    ],
                ),
                # 우측 하단 추가 버튼
                ft.Container(
                    right=30,
                    bottom=30,
                    content=fab,
                ),
            ],
        )

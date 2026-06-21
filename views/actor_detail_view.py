import flet as ft

from repository.actor_repository import ActorRepository
from service.actor_service import ActorService

from components.navigation import AppNavigation


class ActorDetailView:
    # 생성자
    # 선택한 배우의 상세 정보를 표시하기 위한 View
    def __init__(
        self,
        con,
        actor_id,
    ):

        # DuckDB 연결 객체 저장
        self.con = con

        # 선택된 배우 번호 저장
        self.actor_id = actor_id

        # Service 객체 생성
        self.actor_service = ActorService(ActorRepository(con))

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

        # 배우 목록 화면 이동
        elif index == 1:
            from views.actor_view import ActorView

            page.add(ActorView(self.con).build(page))

        # 관람 기록 화면 이동
        elif index == 2:
            from views.record_view import RecordView

            page.add(RecordView(self.con).build(page))

        # 화면 갱신
        page.update()

    # 배우 상세 화면 생성
    def build(
        self,
        page,
    ):

        # 배우 상세 정보 조회
        detail_df = self.actor_service.get_actor_detail(self.actor_id)

        # 배우 정보가 존재하지 않을 경우
        if detail_df.empty:
            return ft.Text("배우 정보를 찾을 수 없습니다.")

        # 배우 기본 정보 추출
        first = detail_df.iloc[0]

        # 출연작 목록 생성
        works = []

        # 배우가 출연한 공연 정보를 반복문으로 추가
        for _, row in detail_df.iterrows():
            works.append(
                ft.Container(
                    bgcolor="#1E293B",
                    border_radius=8,
                    padding=15,
                    margin=5,
                    content=ft.Column(
                        spacing=5,
                        controls=[
                            # 공연 제목
                            ft.Text(
                                row["title"],
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color="white",
                            ),
                            # 배역 정보
                            ft.Text(
                                f"배역 : {row['role_name']}",
                                color="#CBD5E1",
                            ),
                        ],
                    ),
                )
            )

        # 공통 네비게이션 메뉴 생성
        navigation = AppNavigation.build(
            selected_index=1,
            on_change=lambda e: self.change_page(
                page,
                e.control.selected_index,
            ),
        )

        # 배우 상세 화면 반환
        return ft.Row(
            expand=True,
            spacing=0,
            controls=[
                # 좌측 네비게이션
                navigation,
                # 메인 컨텐츠 영역
                ft.Container(
                    expand=True,
                    padding=20,
                    content=ft.Column(
                        expand=True,
                        scroll=ft.ScrollMode.AUTO,
                        controls=[
                            ft.Row(
                                spacing=40,
                                vertical_alignment=ft.CrossAxisAlignment.START,
                                controls=[
                                    # ====================================
                                    # 배우 기본 정보 영역
                                    # ====================================
                                    ft.Column(
                                        controls=[
                                            # 배우 프로필 이미지
                                            ft.Container(
                                                width=320,
                                                height=450,
                                                bgcolor="#1E293B",
                                                border_radius=12,
                                                clip_behavior=ft.ClipBehavior.HARD_EDGE,
                                                content=(
                                                    # 이미지가 존재하는 경우
                                                    ft.Image(
                                                        src=first["profile_image"],
                                                        width=320,
                                                        height=450,
                                                    )
                                                    # 이미지가 없는 경우
                                                    if first["profile_image"]
                                                    else ft.Column(
                                                        expand=True,
                                                        alignment=ft.MainAxisAlignment.CENTER,
                                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                        controls=[
                                                            ft.Text(
                                                                "🎭",
                                                                size=100,
                                                            )
                                                        ],
                                                    )
                                                ),
                                            ),
                                            # 배우 상세 정보 카드
                                            ft.Container(
                                                width=320,
                                                bgcolor="#111827",
                                                border_radius=12,
                                                padding=20,
                                                content=ft.Column(
                                                    controls=[
                                                        # 배우 이름
                                                        ft.Text(
                                                            first["actor_name"],
                                                            size=28,
                                                            weight=ft.FontWeight.BOLD,
                                                            color="white",
                                                        ),
                                                        # 소속사
                                                        ft.Text(
                                                            f"소속사 : {first['agency']}",
                                                            color="white",
                                                        ),
                                                        # 생년월일
                                                        ft.Text(
                                                            f"생년월일 : {first['birth_date']}",
                                                            color="white",
                                                        ),
                                                    ],
                                                ),
                                            ),
                                        ],
                                    ),
                                    # ====================================
                                    # 출연작 목록 영역
                                    # ====================================
                                    ft.Container(
                                        expand=True,
                                        bgcolor="#111827",
                                        border_radius=12,
                                        padding=20,
                                        content=ft.Column(
                                            expand=True,
                                            scroll=ft.ScrollMode.AUTO,
                                            controls=[
                                                # 제목
                                                ft.Text(
                                                    "출연작",
                                                    size=28,
                                                    weight=ft.FontWeight.BOLD,
                                                    color="white",
                                                ),
                                                ft.Divider(),
                                                # 출연작 리스트
                                                *works,
                                            ],
                                        ),
                                    ),
                                ],
                            ),
                        ],
                    ),
                ),
            ],
        )

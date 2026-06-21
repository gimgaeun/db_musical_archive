import flet as ft

from repository.performance_repository import PerformanceRepository
from service.performance_service import PerformanceService

from components.navigation import AppNavigation


class PerformanceDetailView:
    # 생성자
    # 선택한 공연의 상세 정보를 표시하는 화면
    def __init__(
        self,
        con,
        performance_id,
    ):

        # DuckDB 연결 객체 저장
        self.con = con

        # 선택한 공연 번호 저장
        self.performance_id = performance_id

        # 공연 서비스 객체 생성
        self.performance_service = PerformanceService(PerformanceRepository(con))

    # 관람기록 작성 화면 이동
    def open_record_create(
        self,
        page,
    ):

        from views.record_create_view import RecordCreateView

        # 현재 화면 제거
        page.controls.clear()

        # 관람기록 작성 화면 출력
        page.add(
            RecordCreateView(
                self.con,
                self.performance_id,
            ).build(page)
        )

        # 화면 갱신
        page.update()

    # 네비게이션 메뉴 이동
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

        # 관람기록 화면 이동
        elif index == 2:
            from views.record_view import RecordView

            page.add(RecordView(self.con).build(page))

        # 화면 갱신
        page.update()

    # 공연 상세 화면 생성
    def build(
        self,
        page: ft.Page,
    ):

        # 공연 상세 정보 조회
        detail_df = self.performance_service.get_performance_detail(self.performance_id)

        # 공연 정보가 없는 경우
        if detail_df.empty:
            return ft.Text("공연 정보를 찾을 수 없습니다.")

        # 첫 번째 행(공연 기본 정보)
        first = detail_df.iloc[0]

        # 공연 기간 포맷 변경
        start_date = first["start_date"].strftime("%Y.%m.%d")

        end_date = first["end_date"].strftime("%Y.%m.%d")

        # 출연진 목록 생성
        cast_controls = []

        for _, row in detail_df.iterrows():
            cast_controls.append(
                ft.Text(
                    # 배우명 + 배역명 출력
                    f"{row['actor_name']} - {row['role_name']}",
                    size=15,
                    color="white",
                )
            )

        # 공통 네비게이션 생성
        navigation = AppNavigation.build(
            selected_index=0,
            on_change=lambda e: self.change_page(
                page,
                e.control.selected_index,
            ),
        )

        # 메인 컨텐츠 영역
        content = ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Container(
                    padding=20,
                    content=ft.Row(
                        vertical_alignment=ft.CrossAxisAlignment.START,
                        spacing=40,
                        controls=[
                            # ========================
                            # 공연 포스터 영역
                            # ========================
                            ft.Column(
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    # 공연 포스터 출력
                                    ft.Image(
                                        src=first["poster_url"],
                                        width=320,
                                        height=450,
                                    ),
                                    # 공연 제목 출력
                                    ft.Text(
                                        first["title"],
                                        size=28,
                                        weight=ft.FontWeight.BOLD,
                                        color="white",
                                    ),
                                ],
                            ),
                            # ========================
                            # 공연 상세 정보 영역
                            # ========================
                            ft.Container(
                                width=700,
                                bgcolor="#111827",
                                border_radius=12,
                                padding=25,
                                content=ft.Column(
                                    spacing=18,
                                    controls=[
                                        # 제목
                                        ft.Text(
                                            "공연 정보",
                                            size=28,
                                            weight=ft.FontWeight.BOLD,
                                            color="white",
                                        ),
                                        ft.Divider(),
                                        # 공연명
                                        ft.Text(
                                            f"공연명 : {first['title']}",
                                            size=18,
                                            color="white",
                                        ),
                                        # 공연 기간
                                        ft.Text(
                                            f"공연기간 : {start_date} ~ {end_date}",
                                            size=18,
                                            color="white",
                                        ),
                                        # 러닝타임
                                        ft.Text(
                                            f"공연시간 : {first['running_time']}분",
                                            size=18,
                                            color="white",
                                        ),
                                        # 관람 등급
                                        ft.Text(
                                            f"관람등급 : {first['age_limit']}",
                                            size=18,
                                            color="white",
                                        ),
                                        # 공연장명
                                        ft.Text(
                                            f"공연장 : {first['theater_name']}",
                                            size=18,
                                            color="white",
                                        ),
                                        # 공연장 위치
                                        ft.Text(
                                            f"위치 : {first['location']}",
                                            size=18,
                                            color="white",
                                        ),
                                        ft.Divider(),
                                        # 출연진 제목
                                        ft.Text(
                                            "출연진",
                                            size=22,
                                            weight=ft.FontWeight.BOLD,
                                            color="white",
                                        ),
                                        # 출연 배우 목록
                                        *cast_controls,
                                        ft.Container(height=20),
                                        # 관람기록 작성 버튼
                                        ft.ElevatedButton(
                                            "관람기록 작성",
                                            on_click=lambda e: self.open_record_create(
                                                page
                                            ),
                                        ),
                                    ],
                                ),
                            ),
                        ],
                    ),
                )
            ],
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

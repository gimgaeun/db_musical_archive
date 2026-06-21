import flet as ft

from repository.performance_repository import PerformanceRepository
from service.performance_service import PerformanceService

from repository.record_repository import RecordRepository
from service.record_service import RecordService

from components.navigation import AppNavigation


class RecordCreateView:
    # 생성자
    # 관람 기록 작성 화면 초기화
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

        # 관람 기록 서비스 객체 생성
        self.record_service = RecordService(RecordRepository(con))

    # 관람 기록 작성 화면 생성
    def build(
        self,
        page,
    ):

        # 선택한 공연 상세 정보 조회
        performance_df = self.performance_service.get_performance_detail(
            self.performance_id
        )

        # 공연 기본 정보 추출
        first = performance_df.iloc[0]

        # ==========================
        # 입력 컴포넌트 생성
        # ==========================

        # 관람일 입력
        view_date = ft.TextField(
            label="관람일 (2025-06-21)",
            width=350,
        )

        # 관람 캐스트 입력
        cast_name = ft.TextField(
            label="캐스트",
            width=350,
        )

        # 좌석 정보 입력
        seat_info = ft.TextField(
            label="좌석",
            width=350,
        )

        # 티켓 가격 입력
        ticket_price = ft.TextField(
            label="티켓 가격",
            width=350,
        )

        # 평점 선택
        score = ft.Dropdown(
            label="평점",
            width=350,
            options=[
                ft.dropdown.Option("1"),
                ft.dropdown.Option("2"),
                ft.dropdown.Option("3"),
                ft.dropdown.Option("4"),
                ft.dropdown.Option("5"),
            ],
        )

        # 관람 후기 입력
        review = ft.TextField(
            label="후기",
            multiline=True,
            min_lines=5,
            max_lines=8,
            width=500,
        )

        # ==========================
        # 저장 버튼 이벤트
        # ==========================
        def save_record(e):

            # 관람 기록 저장
            self.record_service.save_record(
                1,  # 현재 로그인 사용자 (임시)
                self.performance_id,
                view_date.value,
                int(ticket_price.value),
                seat_info.value,
                cast_name.value,
                int(score.value),
                review.value,
            )

            # 저장 후 관람기록 목록 화면 이동
            from views.record_view import RecordView

            page.controls.clear()

            page.add(RecordView(self.con).build(page))

            page.update()

        # ==========================
        # 화면 구성
        # ==========================
        return ft.Row(
            expand=True,
            controls=[
                # 좌측 네비게이션 메뉴
                AppNavigation.build(
                    selected_index=2,
                ),
                # 메인 컨텐츠 영역
                ft.Container(
                    expand=True,
                    padding=20,
                    content=ft.Row(
                        spacing=40,
                        controls=[
                            # ====================
                            # 공연 정보 영역
                            # ====================
                            ft.Column(
                                controls=[
                                    # 공연 포스터 출력
                                    ft.Image(
                                        src=first["poster_url"],
                                        width=250,
                                        height=350,
                                    ),
                                    # 공연 제목 출력
                                    ft.Text(
                                        first["title"],
                                        size=24,
                                        weight=ft.FontWeight.BOLD,
                                        color="white",
                                    ),
                                ],
                            ),
                            # ====================
                            # 관람 기록 입력 영역
                            # ====================
                            ft.Column(
                                spacing=15,
                                controls=[
                                    view_date,
                                    cast_name,
                                    seat_info,
                                    ticket_price,
                                    score,
                                    review,
                                    # 저장 버튼
                                    ft.ElevatedButton(
                                        "저장",
                                        on_click=save_record,
                                    ),
                                ],
                            ),
                        ],
                    ),
                ),
            ],
        )

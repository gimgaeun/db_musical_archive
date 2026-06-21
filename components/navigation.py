import flet as ft


class AppNavigation:
    # 정적 메서드
    # 객체를 생성하지 않고 AppNavigation.build() 형태로 호출 가능
    @staticmethod
    def build(
        selected_index=0,  # 현재 선택된 메뉴 인덱스
        on_change=None,  # 메뉴 선택 시 실행될 이벤트 함수
    ):

        # 왼쪽 네비게이션 메뉴 생성
        return ft.NavigationRail(
            # 현재 선택된 메뉴
            selected_index=selected_index,
            # 네비게이션 최소 너비
            min_width=80,
            # 배경 색상
            bgcolor="#0F172A",
            # 메뉴 변경 이벤트
            on_change=on_change,
            # 메뉴 목록
            destinations=[
                # 홈 메뉴
                ft.NavigationRailDestination(
                    icon=ft.Icons.HOME,
                    label="홈",
                ),
                # 배우 메뉴
                ft.NavigationRailDestination(
                    icon=ft.Icons.PERSON,
                    label="배우",
                ),
                # 관람 기록 메뉴
                ft.NavigationRailDestination(
                    icon=ft.Icons.BOOK,
                    label="기록",
                ),
                # 관심 공연(즐겨찾기) 메뉴
                ft.NavigationRailDestination(
                    icon=ft.Icons.STAR,
                    label="즐찾",
                ),
                # 통계 메뉴
                ft.NavigationRailDestination(
                    icon=ft.Icons.BAR_CHART,
                    label="통계",
                ),
            ],
        )

import flet as ft

from repository.record_repository import RecordRepository
from service.record_service import RecordService

from components.navigation import AppNavigation


class RecordView:
    def __init__(self, con):

        self.con = con

        self.record_service = RecordService(RecordRepository(con))
        print("RECORD VIEW LOADED")

    def change_page(
        self,
        page,
        index,
    ):

        page.controls.clear()

        if index == 0:
            from views.main_view import MainView

            page.add(MainView(self.con).build(page))

        elif index == 1:
            from views.actor_view import ActorView

            page.add(ActorView(self.con).build(page))

        elif index == 2:
            page.add(RecordView(self.con).build(page))

        page.update()

    def build(
        self,
        page,
    ):

        record_df = self.record_service.get_all_records()

        cards = []

        for _, row in record_df.iterrows():
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
                        ft.Image(
                            src=row["poster_url"],
                            width=180,
                            height=250,
                        ),
                        ft.Text(
                            row["title"],
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color="white",
                        ),
                        ft.Text(
                            row["view_date"].strftime("%Y.%m.%d"),
                            size=11,
                            color="#94A3B8",
                        ),
                        ft.Text(
                            stars,
                            color="#FACC15",
                            size=16,
                        ),
                    ],
                ),
            )

            cards.append(card)

        navigation = AppNavigation.build(
            selected_index=2,
            on_change=lambda e: self.change_page(
                page,
                e.control.selected_index,
            ),
        )

        content = ft.Container(
            expand=True,
            padding=20,
            content=ft.Column(
                spacing=20,
                controls=[
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
                    ft.Row(
                        wrap=True,
                        spacing=20,
                        run_spacing=20,
                        controls=cards,
                    ),
                    ft.Container(expand=True),
                ],
            ),
        )

        fab = ft.FloatingActionButton(
            icon=ft.Icons.ADD,
        )

        return ft.Stack(
            expand=True,
            controls=[
                ft.Row(
                    expand=True,
                    spacing=0,
                    controls=[
                        navigation,
                        content,
                    ],
                ),
                ft.Container(
                    right=30,
                    bottom=30,
                    content=fab,
                ),
            ],
        )
    

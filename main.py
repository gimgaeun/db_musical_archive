import duckdb
import flet as ft

from views.main_view import MainView


def main(page: ft.Page):

    page.title = "Musical Archive"

    page.padding = 0
    page.bgcolor = "#020617"

    page.window.width = 1000
    page.window.height = 600

    page.window_resizable = False

    con = duckdb.connect("data/musical_archive.db")

    page.add(MainView(con).build(page))


ft.app(target=main)

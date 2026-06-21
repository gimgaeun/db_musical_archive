import duckdb

from database.create_table import create_table
from database.seed_data import insert_dummy_data


def main():
    print("[INFO] DuckDB 연결")
    con = duckdb.connect("data/musical_archive.db")

    create_table(con)

    insert_dummy_data(con)

    con.close()

    print("[INFO] 프로그램 종료")


if __name__ == "__main__":
    main()

# endregion

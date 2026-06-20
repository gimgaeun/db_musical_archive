import duckdb

# =========================================================================
# region: DuckDB Database Operations
# =========================================================================


def create_table(con: duckdb.DuckDBPyConnection):
    """
    Musical Archive 테이블 생성
    """
    print("[INFO] DuckDB 테이블 생성 시작")

    query = """
    -- 1. User 테이블 생성
    CREATE TABLE IF NOT EXISTS Users(
        user_id BIGINT PRIMARY KEY,
        email VARCHAR UNIQUE NOT NULL,
        password VARCHAR NOT NULL,
        nickname VARCHAR UNIQUE NOT NULL,
        join_date DATE 
    );

    -- 2. Theater 테이블 생성
    CREATE TABLE IF NOT EXISTS Theater (
        theater_id BIGINT PRIMARY KEY,
        theater_name VARCHAR UNIQUE NOT NULL,
        location VARCHAR,
        seat_count INTEGER
    );

    -- 3. Performance 테이블 생성
    CREATE TABLE IF NOT EXISTS Performance (
        performance_id BIGINT PRIMARY KEY,
        title VARCHAR NOT NULL,
        start_date DATE,
        end_date DATE,
        running_time INTEGER,
        age_limit VARCHAR,
        poster_url VARCHAR,
        theater_id BIGINT,

        FOREIGN KEY (theater_id)
        REFERENCES Theater(theater_id)
    );

    -- 4. Actor 테이블 생성
    CREATE TABLE IF NOT EXISTS Actor (
        actor_id BIGINT PRIMARY KEY,
        actor_name VARCHAR NOT NULL,
        birth_date DATE,
        profile_image VARCHAR,
        agency VARCHAR
    );

    -- 5. Casting 테이블 생성
    CREATE TABLE IF NOT EXISTS Casting (
        performance_id BIGINT,
        actor_id BIGINT,
        role_name VARCHAR,

        PRIMARY KEY (performance_id, actor_id),

        FOREIGN KEY (performance_id)
        REFERENCES Performance(performance_id),

        FOREIGN KEY (actor_id)
        REFERENCES Actor(actor_id)
    );

    -- 6. Record 테이블 생성
    CREATE TABLE IF NOT EXISTS Record (
        record_id BIGINT PRIMARY KEY,

        user_id BIGINT NOT NULL,
        performance_id BIGINT NOT NULL,

        view_date DATE,
        ticket_price INTEGER,

        seat_info VARCHAR,
        cast_name VARCHAR,

        score INTEGER,
        review VARCHAR,

        FOREIGN KEY (user_id)
        REFERENCES Users(user_id),

        FOREIGN KEY (performance_id)
        REFERENCES Performance(performance_id)
    );

    -- 7. Favorite 테이블 생성
    CREATE TABLE IF NOT EXISTS Favorite (
        user_id BIGINT,
        performance_id BIGINT,

        PRIMARY KEY (user_id, performance_id),

        FOREIGN KEY (user_id)
        REFERENCES Users(user_id),

        FOREIGN KEY (performance_id)
        REFERENCES Performance(performance_id)
    );
    """

    con.execute(query)
    print("[INFO] DuckDB 테이블 생성 완료")


# endregion


# =========================================================================
# region: Main
# =========================================================================


def main():
    con = duckdb.connect("data/musical_archive.db")

    create_table(con)


if __name__ == "__main__":
    main()

# endregion

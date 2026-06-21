import duckdb

# =========================================================================
# region: DuckDB Database Operations
# =========================================================================


def create_table(con: duckdb.DuckDBPyConnection):
    """
    Musical Archive 프로젝트의 테이블 생성
    """

    print("[INFO] DuckDB 테이블 생성 시작")

    query = """

    -- ==========================================================
    -- 1. 사용자 정보 테이블
    -- 회원가입한 사용자의 정보를 저장
    -- ==========================================================
    CREATE TABLE IF NOT EXISTS Users(

        -- 사용자 고유 번호
        user_id BIGINT PRIMARY KEY,

        -- 이메일 (중복 불가)
        email VARCHAR UNIQUE NOT NULL,

        -- 비밀번호
        password VARCHAR NOT NULL,

        -- 닉네임 (중복 불가)
        nickname VARCHAR UNIQUE NOT NULL,

        -- 가입일
        join_date DATE
    );


    -- ==========================================================
    -- 2. 공연장 정보 테이블
    -- 공연장의 기본 정보를 저장
    -- ==========================================================
    CREATE TABLE IF NOT EXISTS Theater (

        -- 공연장 고유 번호
        theater_id BIGINT PRIMARY KEY,

        -- 공연장 이름
        theater_name VARCHAR UNIQUE NOT NULL,

        -- 공연장 위치
        location VARCHAR,

        -- 좌석 수
        seat_count INTEGER
    );


    -- ==========================================================
    -- 3. 공연 정보 테이블
    -- 뮤지컬 공연 정보를 저장
    -- ==========================================================
    CREATE TABLE IF NOT EXISTS Performance (

        -- 공연 고유 번호
        performance_id BIGINT PRIMARY KEY,

        -- 공연 제목
        title VARCHAR NOT NULL,

        -- 공연 시작일
        start_date DATE,

        -- 공연 종료일
        end_date DATE,

        -- 러닝타임(분)
        running_time INTEGER,

        -- 관람 등급
        age_limit VARCHAR,

        -- 공연 포스터 이미지 경로
        poster_url VARCHAR,

        -- 공연장 번호
        theater_id BIGINT,

        -- 공연장 정보 참조
        FOREIGN KEY (theater_id)
        REFERENCES Theater(theater_id)
    );


    -- ==========================================================
    -- 4. 배우 정보 테이블
    -- 뮤지컬 배우 정보를 저장
    -- ==========================================================
    CREATE TABLE IF NOT EXISTS Actor (

        -- 배우 고유 번호
        actor_id BIGINT PRIMARY KEY,

        -- 배우 이름
        actor_name VARCHAR NOT NULL,

        -- 생년월일
        birth_date DATE,

        -- 프로필 이미지 경로
        profile_image VARCHAR,

        -- 소속사
        agency VARCHAR
    );


    -- ==========================================================
    -- 5. 캐스팅 정보 테이블
    -- 공연과 배우의 다대다(M:N) 관계를 연결
    -- ==========================================================
    CREATE TABLE IF NOT EXISTS Casting (

        -- 공연 번호
        performance_id BIGINT,

        -- 배우 번호
        actor_id BIGINT,

        -- 배역명
        role_name VARCHAR,

        -- 복합 기본키
        PRIMARY KEY (
            performance_id,
            actor_id
        ),

        -- 공연 정보 참조
        FOREIGN KEY (performance_id)
        REFERENCES Performance(performance_id),

        -- 배우 정보 참조
        FOREIGN KEY (actor_id)
        REFERENCES Actor(actor_id)
    );


    -- ==========================================================
    -- 6. 관람 기록 테이블
    -- 사용자가 관람한 공연 정보를 저장
    -- ==========================================================
    CREATE TABLE IF NOT EXISTS Record (

        -- 관람 기록 번호
        record_id BIGINT PRIMARY KEY,

        -- 사용자 번호
        user_id BIGINT NOT NULL,

        -- 공연 번호
        performance_id BIGINT NOT NULL,

        -- 관람일
        view_date DATE,

        -- 티켓 가격
        ticket_price INTEGER,

        -- 좌석 정보
        seat_info VARCHAR,

        -- 관람한 캐스트 정보
        cast_name VARCHAR,

        -- 평점
        score INTEGER,

        -- 후기
        review VARCHAR,

        -- 사용자 정보 참조
        FOREIGN KEY (user_id)
        REFERENCES Users(user_id),

        -- 공연 정보 참조
        FOREIGN KEY (performance_id)
        REFERENCES Performance(performance_id)
    );


    -- ==========================================================
    -- 7. 관심 공연 테이블
    -- 사용자가 즐겨찾기한 공연 저장
    -- ==========================================================
    CREATE TABLE IF NOT EXISTS Favorite (

        -- 사용자 번호
        user_id BIGINT,

        -- 공연 번호
        performance_id BIGINT,

        -- 한 사용자는 같은 공연을 한 번만 등록 가능
        PRIMARY KEY (
            user_id,
            performance_id
        ),

        -- 사용자 정보 참조
        FOREIGN KEY (user_id)
        REFERENCES Users(user_id),

        -- 공연 정보 참조
        FOREIGN KEY (performance_id)
        REFERENCES Performance(performance_id)
    );
    """

    # SQL 실행
    con.execute(query)

    print("[INFO] DuckDB 테이블 생성 완료")


# endregion

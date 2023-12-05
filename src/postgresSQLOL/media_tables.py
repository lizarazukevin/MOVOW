""" create tables in the PostgreSQL database """
commands = (
    """
    CREATE TABLE movies (
        movie_id        INT                 GENERATED ALWAYS AS IDENTITY,
        tag             VARCHAR(255)        NOT NULL,
        movie_title     VARCHAR(255)        NOT NULL,
        original_title  VARCHAR(255),
        release_date    DATE,
        runtime         INT,
        status          VARCHAR(255),
        audience_rating FLOAT,
        num_ratings     INT,
        PRIMARY KEY (movie_id),
        UNIQUE (tag)
    )
    """,

    """
    CREATE TABLE shows (
        show_id         INT                 GENERATED ALWAYS AS IDENTITY,
        tag             VARCHAR(255)        NOT NULL,
        show_title      VARCHAR(255)        NOT NULL,
        original_title  VARCHAR(255),
        initial_release DATE,
        final_release   DATE,
        num_episodes    INT,
        num_seasons     INT,
        in_production   BOOL,
        status          VARCHAR(255),
        PRIMARY KEY (show_id),
        UNIQUE(tag)
    )
    """,

    """
    CREATE TABLE seasons (
        season_id       INT                 GENERATED ALWAYS AS IDENTITY,
        show_id         INT                 NOT NULL,
        tag             VARCHAR(255)        NOT NULL,
        season_title    VARCHAR(255)        NOT NULL,
        chron_order     INT,
        num_episodes    INT,
        audience_rating FLOAT,
        num_ratings     INT,
        PRIMARY KEY (season_id),
        FOREIGN KEY (show_id) 
            REFERENCES shows(show_id)
            ON UPDATE CASCADE ON DELETE CASCADE
    )
    """,

    """
    CREATE TABLE episodes (
        episode_id      INT                 GENERATED ALWAYS AS IDENTITY,
        season_id       INT                 NOT NULL,
        tag             VARCHAR(255)        NOT NULL,
        episode_title   VARCHAR(255)        NOT NULL,
        chron_order     INT,
        runtime         INT,
        audience_rating FLOAT,
        num_ratings     INT,
        PRIMARY KEY (episode_id),
        FOREIGN KEY (season_id) 
            REFERENCES seasons(season_id)
            ON UPDATE CASCADE ON DELETE CASCADE
    )
    """,

    """
    CREATE TABLE genres (
        genre_id        INT                 GENERATED ALWAYS AS IDENTITY,
        genre_name      VARCHAR(255)        NOT NULL,
        PRIMARY KEY (genre_id),
        UNIQUE (genre_name)
    )
    """,

    """
    CREATE TABLE movie_genres (
        movie_id        INT,
        genre_id        INT,
        FOREIGN KEY (movie_id) 
            REFERENCES movies(movie_id)
            ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY (genre_id) 
            REFERENCES genres(genre_id)
            ON UPDATE CASCADE ON DELETE CASCADE
    )
    """,

    """
    CREATE TABLE show_genres (
        show_id         INT,
        genre_id        INT,
        FOREIGN KEY (show_id) 
            REFERENCES shows(show_id)
            ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY (genre_id) 
            REFERENCES genres(genre_id)
            ON UPDATE CASCADE ON DELETE CASCADE
    )
    """,

    """
    CREATE TABLE people (
        person_id       INT                 GENERATED ALWAYS AS IDENTITY,
        tag             VARCHAR(255)        NOT NULL,
        person_name     VARCHAR(255)        NOT NULL,
        birthday        DATE,
        death           DATE,
        gender          INT,
        department      VARCHAR(255),
        PRIMARY KEY (person_id),
        UNIQUE (tag)
    )
    """,

    """
    CREATE TABLE people_aliases (
        person_id       INT,
        name            VARCHAR(255),
        FOREIGN KEY (person_id) 
            REFERENCES people(person_id)
            ON UPDATE CASCADE ON DELETE CASCADE
    )
    """,

    """
    CREATE TABLE movie_casting_credits (
        credit_id       SERIAL              NOT NULL,
        movie_id        INT                 NOT NULL,
        person_id       INT                 NOT NULL,
        character       VARCHAR(255),
        PRIMARY KEY (credit_id),
        FOREIGN KEY (movie_id) 
            REFERENCES movies(movie_id)
            ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY (person_id) 
            REFERENCES people(person_id)
            ON UPDATE CASCADE ON DELETE CASCADE
    )
    """,

    """
    CREATE TABLE movie_crew_credits (
        credit_id       SERIAL              NOT NULL,
        movie_id        INT                 NOT NULL,
        person_id       INT                 NOT NULL,
        department      VARCHAR(255),
        job             VARCHAR(255),
        PRIMARY KEY (credit_id),
        FOREIGN KEY (movie_id) 
            REFERENCES movies(movie_id)
            ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY (person_id) 
            REFERENCES people(person_id)
            ON UPDATE CASCADE ON DELETE CASCADE
    )
    """,

    """
    CREATE TABLE show_casting_credits (
        credit_id       SERIAL              NOT NULL,
        show_id         INT                 NOT NULL,
        person_id       INT                 NOT NULL,
        character       VARCHAR(255),
        PRIMARY KEY (credit_id),
        FOREIGN KEY (show_id) 
            REFERENCES shows(show_id)
            ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY (person_id) 
            REFERENCES people(person_id)
            ON UPDATE CASCADE ON DELETE CASCADE
    )
    """,

    """
    CREATE TABLE show_crew_credits (
        credit_id       SERIAL              NOT NULL,
        show_id        INT                 NOT NULL,
        person_id       INT                 NOT NULL,
        department      VARCHAR(255),
        job             VARCHAR(255),
        PRIMARY KEY (credit_id),
        FOREIGN KEY (show_id) 
            REFERENCES shows(show_id)
            ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY (person_id) 
            REFERENCES people(person_id)
            ON UPDATE CASCADE ON DELETE CASCADE
    )
    """,

    """
    CREATE TABLE season_casting_credits (
        credit_id       SERIAL              NOT NULL,
        season_id       INT                 NOT NULL,
        person_id       INT                 NOT NULL,
        character       VARCHAR(255),
        PRIMARY KEY (credit_id),
        FOREIGN KEY (season_id) 
            REFERENCES seasons(season_id)
            ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY (person_id) 
            REFERENCES people(person_id)
            ON UPDATE CASCADE ON DELETE CASCADE
    )
    """,

    """
    CREATE TABLE season_crew_credits (
        credit_id       SERIAL              NOT NULL,
        season_id       INT                 NOT NULL,
        person_id       INT                 NOT NULL,
        department      VARCHAR(255),
        job             VARCHAR(255),
        PRIMARY KEY (credit_id),
        FOREIGN KEY (season_id) 
            REFERENCES seasons(season_id)
            ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY (person_id) 
            REFERENCES people(person_id)
            ON UPDATE CASCADE ON DELETE CASCADE
    )
    """,

    """
    CREATE TABLE movie_reviews (
        review_id       SERIAL              NOT NULL,
        movie_id        INT                 NOT NULL,
        tag             VARCHAR(255)        NOT NULL,
        author_name     VARCHAR(255),
        author_username VARCHAR(255),
        rating          FLOAT,
        content         VARCHAR(4095),
        time_created    TIMESTAMP,
        time_updated    TIMESTAMP,
        origin          VARCHAR(255)        NOT NULL,
        reference       VARCHAR(2047)       NOT NULL,
        PRIMARY KEY (review_id),
        FOREIGN KEY (movie_id) 
            REFERENCES movies(movie_id)
            ON UPDATE CASCADE ON DELETE CASCADE,
        UNIQUE (tag)
    )
    """,

    """
    CREATE TABLE show_reviews (
        review_id       SERIAL              NOT NULL,
        show_id         INT                 NOT NULL,
        tag             VARCHAR(255)        NOT NULL,
        author_name     VARCHAR(255),
        author_username VARCHAR(255),
        rating          FLOAT,
        content         VARCHAR(4095),
        time_created    TIMESTAMP,
        time_updated    TIMESTAMP,
        origin          VARCHAR(255)        NOT NULL,
        reference       VARCHAR(2047)       NOT NULL,
        PRIMARY KEY (review_id),
        FOREIGN KEY (show_id) 
            REFERENCES shows(show_id)
            ON UPDATE CASCADE ON DELETE CASCADE,
        UNIQUE (tag)
    )
    """,

    """
    CREATE TABLE regions (
        region_id       INT                 GENERATED ALWAYS AS IDENTITY, 
        iso             VARCHAR(255)        NOT NULL,
        PRIMARY KEY (region_id),
        UNIQUE (iso)
    )
    """,

    """
    CREATE TABLE providers (
        provider_id     INT                 GENERATED ALWAYS AS IDENTITY,
        provider_name   VARCHAR(255)        NOT NULL,
        PRIMARY KEY (provider_id),
        UNIQUE (provider_name)
    )
    """,

    """
    CREATE TABLE region_provided_movies (
        movie_id        INT                 NOT NULL,
        region_id       INT                 NOT NULL,
        provider_id     INT                 NOT NULL,
        rent            BOOL                NOT NULL,
        rent_price      FLOAT,
        buy             BOOL                NOT NULL,
        buy_price       FLOAT,
        flatrate        BOOL                NOT NULL,
        flatrate_price  FLOAT,
        FOREIGN KEY (movie_id) 
            REFERENCES movies(movie_id)
            ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY (region_id) 
            REFERENCES regions(region_id)
            ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY (provider_id)
            REFERENCES providers(provider_id)
            ON UPDATE CASCADE ON DELETE CASCADE
    )
    """,

    """
    CREATE TABLE region_provided_shows (
        show_id         INT                 NOT NULL,
        region_id       INT                 NOT NULL,
        provider_id     INT                 NOT NULL,
        rent            BOOL                NOT NULL,
        rent_price      FLOAT,
        buy             BOOL                NOT NULL,
        buy_price       FLOAT,
        flatrate        BOOL                NOT NULL,
        flatrate_price  FLOAT,
        FOREIGN KEY (show_id) 
            REFERENCES shows(show_id)
            ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY (region_id) 
            REFERENCES regions(region_id)
            ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY (provider_id)
            REFERENCES providers(provider_id)
            ON UPDATE CASCADE ON DELETE CASCADE
    )
    """,

    """
    CREATE TABLE region_provided_seasons (
        season_id       INT                 NOT NULL,
        region_id       INT                 NOT NULL,
        provider_id     INT                 NOT NULL,
        rent            BOOL                NOT NULL,
        rent_price      FLOAT,
        buy             BOOL                NOT NULL,
        buy_price       FLOAT,
        flatrate        BOOL                NOT NULL,
        flatrate_price  FLOAT,
        FOREIGN KEY (season_id) 
            REFERENCES seasons(season_id)
            ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY (region_id) 
            REFERENCES regions(region_id)
            ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY (provider_id)
            REFERENCES providers(provider_id)
            ON UPDATE CASCADE ON DELETE CASCADE
    )
    """
)
""" create tables in the PostgreSQL database """
commands = (
    """
    CREATE TABLE account (
        account_id      INT                 GENERATED ALWAYS AS IDENTITY,
        username        VARCHAR(255)        NOT NULL,
        password        VARCHAR(255)        NOT NULL,
        first_name      VARCHAR(255),
        last_name       VARCHAR(255),
        email           VARCHAR(255)        NOT NULL,
        birth           DATE                NOT NULL,
        date_joined     DATE                NOT NULL,
        last_login      DATE                NOT NULL,
        gender          INT,
        pro             BOOL                NOT NULL,
        private         BOOL                NOT NULL,
        avatar_url      VARCHAR(2047),
        PRIMARY KEY (account_id),
        UNIQUE (username, email)
    )
    """,
    """
    CREATE TABLE address (
        account_id      INT                 NOT NULL,
        country         VARCHAR(255),
        street          VARCHAR(255),
        city            VARCHAR(255),
        state           VARCHAR(15),
        zip             INT,
        FOREIGN KEY (account_id) 
            REFERENCES account(account_id)
            ON UPDATE CASCADE ON DELETE CASCADE
    )
    """
)
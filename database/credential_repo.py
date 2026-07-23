from database.db import get_connection


def save_credential(session_id, username, password):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO credentials
        (
            session_id,
            username,
            password
        )
        VALUES
        (
            %s,
            %s,
            %s
        )
    """, (session_id, username, password))

    connection.commit()

    cursor.close()
    connection.close()
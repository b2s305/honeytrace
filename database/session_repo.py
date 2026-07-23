from database.db import get_connection


def create_session(attacker_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO sessions
        (
            attacker_id,
            service,
            start_time
        )
        VALUES
        (
            %s,
            'SSH',
            NOW()
        )
    """, (attacker_id,))

    connection.commit()

    session_id = cursor.lastrowid

    cursor.close()
    connection.close()

    return session_id
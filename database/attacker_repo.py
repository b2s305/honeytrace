from database.db import get_connection


def save_attacker(ip_address):

    connection = get_connection()
    cursor = connection.cursor()

    # Check if attacker already exists
    cursor.execute(
        "SELECT id FROM attackers WHERE ip_address=%s",
        (ip_address,)
    )

    result = cursor.fetchone()

    if result:
        attacker_id = result[0]

        cursor.execute(
            "UPDATE attackers SET last_seen=NOW() WHERE id=%s",
            (attacker_id,)
        )

    else:

        cursor.execute("""
            INSERT INTO attackers
            (
                ip_address,
                first_seen,
                last_seen,
                risk_score
            )
            VALUES
            (
                %s,
                NOW(),
                NOW(),
                0
            )
        """, (ip_address,))

        attacker_id = cursor.lastrowid

    connection.commit()

    cursor.close()
    connection.close()

    return attacker_id
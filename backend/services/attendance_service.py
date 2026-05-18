from datetime import datetime

from backend.database.db import get_connection


class AttendanceService:

    def __init__(self):

        self.conn = get_connection()

        self.cursor = self.conn.cursor()

    def mark_attendance(self, name):

        now = datetime.now()

        date = now.strftime("%Y-%m-%d")

        current_time = now.strftime("%H:%M:%S")

        self.cursor.execute(
            """
            SELECT * FROM attendance
            WHERE name=? AND date=?
            """,
            (name, date)
        )

        result = self.cursor.fetchone()

        # FIRST ENTRY

        if result is None:

            self.cursor.execute(
                """
                INSERT INTO attendance
                (
                    employee_id,
                    name,
                    date,
                    first_in,
                    last_out
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    name,
                    name,
                    date,
                    current_time,
                    current_time
                )
            )

            self.cursor.execute(
                """
                INSERT INTO movement_log
                (
                    name,
                    date,
                    time,
                    event
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    name,
                    date,
                    current_time,
                    "IN"
                )
            )

            self.conn.commit()

            print(f"[IN] {name}")

        else:

            self.cursor.execute(
                """
                UPDATE attendance
                SET last_out=?
                WHERE name=? AND date=?
                """,
                (
                    current_time,
                    name,
                    date
                )
            )

            self.cursor.execute(
                """
                INSERT INTO movement_log
                (
                    name,
                    date,
                    time,
                    event
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    name,
                    date,
                    current_time,
                    "OUT"
                )
            )

            self.conn.commit()

            print(f"[OUT] {name}")
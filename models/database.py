"""
AquaPulse – Database Layer
==========================
SQLite-backed persistence for water-parameter readings with full CRUD
operations, CSV export/import, and pandas DataFrame retrieval.

All queries use parameterised placeholders to prevent SQL injection.
"""

import csv
import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Generator, List, Optional

import pandas as pd

from utils.constants import DB_FILENAME


class DatabaseManager:
    """Manages every SQLite interaction for AquaPulse."""

    _CREATE_TABLE_SQL = """
    CREATE TABLE IF NOT EXISTS readings (
        id                      INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp               TEXT    NOT NULL,
        ammonia_ppm             REAL    NOT NULL,
        nitrite_ppm             REAL    NOT NULL,
        nitrate_ppm             REAL    NOT NULL,
        ph                      REAL    NOT NULL,
        temperature_c           REAL    NOT NULL,
        water_changed           INTEGER NOT NULL DEFAULT 0,
        water_change_volume_pct REAL    DEFAULT 0.0,
        notes                   TEXT    DEFAULT ''
    );
    """

    _CREATE_INDEX_SQL = """
    CREATE INDEX IF NOT EXISTS idx_readings_timestamp
    ON readings (timestamp);
    """

    _CREATE_PROFILE_SQL = """
    CREATE TABLE IF NOT EXISTS aquarium_profile (
        id                  INTEGER PRIMARY KEY CHECK (id = 1),
        tank_name           TEXT    DEFAULT 'My Aquarium',
        tank_size_liters    REAL    DEFAULT 19.0,
        fish_species        TEXT    DEFAULT 'betta',
        created_at          TEXT    NOT NULL,
        updated_at          TEXT    NOT NULL
    );
    """

    # ─── Lifecycle ───────────────────────────────────────────────────────

    def __init__(self, db_path: Optional[str] = None) -> None:
        """
        Open (or create) the SQLite database at *db_path*.

        Args:
            db_path: Filesystem path to the ``.db`` file.
                     Defaults to ``aquapulse.db`` in the working directory.
        """
        self._db_path: str = db_path or DB_FILENAME
        self._connection: Optional[sqlite3.Connection] = None
        self._initialise()

    def _initialise(self) -> None:
        """Create the connection, enable WAL mode, and ensure the schema."""
        try:
            self._connection = sqlite3.connect(self._db_path)
            self._connection.row_factory = sqlite3.Row
            self._connection.execute("PRAGMA journal_mode=WAL;")
            self._connection.execute(self._CREATE_TABLE_SQL)
            self._connection.execute(self._CREATE_INDEX_SQL)
            self._connection.execute(self._CREATE_PROFILE_SQL)
            self._connection.commit()
        except sqlite3.Error as exc:
            raise RuntimeError(
                f"Failed to initialise database at '{self._db_path}': {exc}"
            ) from exc

    @contextmanager
    def _cursor(self) -> Generator[sqlite3.Cursor, None, None]:
        """Yield a cursor inside an auto-commit / auto-rollback block."""
        if self._connection is None:
            raise RuntimeError("Database connection is closed.")
        cursor = self._connection.cursor()
        try:
            yield cursor
            self._connection.commit()
        except sqlite3.Error:
            self._connection.rollback()
            raise
        finally:
            cursor.close()

    def close(self) -> None:
        """Safely close the database connection."""
        if self._connection is not None:
            try:
                self._connection.close()
            except sqlite3.Error:
                pass
            finally:
                self._connection = None

    # ─── CREATE ──────────────────────────────────────────────────────────

    def insert_reading(
        self,
        ammonia_ppm: float,
        nitrite_ppm: float,
        nitrate_ppm: float,
        ph: float,
        temperature_c: float,
        water_changed: bool = False,
        water_change_volume_pct: float = 0.0,
        notes: str = "",
        timestamp: Optional[str] = None,
    ) -> int:
        """
        Insert a new water-parameter reading.

        Args:
            ammonia_ppm:  Ammonia concentration in ppm.
            nitrite_ppm:  Nitrite concentration in ppm.
            nitrate_ppm:  Nitrate concentration in ppm.
            ph:           pH level.
            temperature_c: Water temperature in °C.
            water_changed: Whether a water change was performed.
            water_change_volume_pct: Percentage of water replaced (0–100).
            notes:        Free-form observation notes.
            timestamp:    ISO-formatted timestamp string.  Defaults to *now*.

        Returns:
            The ``ROWID`` of the newly inserted record.
        """
        ts = timestamp or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = """
            INSERT INTO readings
                (timestamp, ammonia_ppm, nitrite_ppm, nitrate_ppm,
                 ph, temperature_c, water_changed,
                 water_change_volume_pct, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        try:
            with self._cursor() as cur:
                cur.execute(
                    sql,
                    (
                        ts,
                        ammonia_ppm,
                        nitrite_ppm,
                        nitrate_ppm,
                        ph,
                        temperature_c,
                        int(water_changed),
                        water_change_volume_pct,
                        notes,
                    ),
                )
                return cur.lastrowid or 0
        except sqlite3.Error as exc:
            raise RuntimeError(f"Failed to insert reading: {exc}") from exc

    # ─── READ ────────────────────────────────────────────────────────────

    def get_all_readings(self) -> List[Dict[str, Any]]:
        """Return every reading as a list of dicts, oldest first."""
        sql = "SELECT * FROM readings ORDER BY timestamp ASC;"
        try:
            with self._cursor() as cur:
                cur.execute(sql)
                return [dict(row) for row in cur.fetchall()]
        except sqlite3.Error as exc:
            raise RuntimeError(f"Failed to fetch readings: {exc}") from exc

    def get_reading_by_id(self, reading_id: int) -> Optional[Dict[str, Any]]:
        """Return a single reading by primary key, or ``None``."""
        sql = "SELECT * FROM readings WHERE id = ?;"
        try:
            with self._cursor() as cur:
                cur.execute(sql, (reading_id,))
                row = cur.fetchone()
                return dict(row) if row else None
        except sqlite3.Error as exc:
            raise RuntimeError(
                f"Failed to fetch reading {reading_id}: {exc}"
            ) from exc

    def get_latest_reading(self) -> Optional[Dict[str, Any]]:
        """Return the most recent reading, or ``None`` if the table is empty."""
        sql = "SELECT * FROM readings ORDER BY timestamp DESC LIMIT 1;"
        try:
            with self._cursor() as cur:
                cur.execute(sql)
                row = cur.fetchone()
                return dict(row) if row else None
        except sqlite3.Error as exc:
            raise RuntimeError(
                f"Failed to fetch latest reading: {exc}"
            ) from exc

    def get_readings_by_date_range(
        self, start_date: str, end_date: str
    ) -> List[Dict[str, Any]]:
        """
        Return readings whose ``DATE(timestamp)`` falls within
        [*start_date*, *end_date*] (inclusive, ``YYYY-MM-DD``).
        """
        sql = """
            SELECT * FROM readings
            WHERE DATE(timestamp) BETWEEN DATE(?) AND DATE(?)
            ORDER BY timestamp ASC;
        """
        try:
            with self._cursor() as cur:
                cur.execute(sql, (start_date, end_date))
                return [dict(row) for row in cur.fetchall()]
        except sqlite3.Error as exc:
            raise RuntimeError(
                f"Failed to fetch readings by date range: {exc}"
            ) from exc

    def get_readings_as_dataframe(self) -> pd.DataFrame:
        """Load all readings into a :class:`pandas.DataFrame` with parsed timestamps."""
        if self._connection is None:
            raise RuntimeError("Database connection is closed.")
        try:
            df = pd.read_sql_query(
                "SELECT * FROM readings ORDER BY timestamp ASC;",
                self._connection,
                parse_dates=["timestamp"],
            )
            return df
        except Exception as exc:
            raise RuntimeError(f"Failed to build DataFrame: {exc}") from exc

    def search_readings(self, query: str) -> List[Dict[str, Any]]:
        """
        Full-text search across ``notes`` and ``timestamp`` columns.

        Args:
            query: Substring to match (case-insensitive via SQLite LIKE).

        Returns:
            Matching readings ordered newest-first.
        """
        sql = """
            SELECT * FROM readings
            WHERE notes LIKE ? OR timestamp LIKE ?
            ORDER BY timestamp DESC;
        """
        wildcard = f"%{query}%"
        try:
            with self._cursor() as cur:
                cur.execute(sql, (wildcard, wildcard))
                return [dict(row) for row in cur.fetchall()]
        except sqlite3.Error as exc:
            raise RuntimeError(f"Search failed: {exc}") from exc

    def get_reading_count(self) -> int:
        """Return the total number of stored readings."""
        sql = "SELECT COUNT(*) FROM readings;"
        try:
            with self._cursor() as cur:
                cur.execute(sql)
                result = cur.fetchone()
                return result[0] if result else 0
        except sqlite3.Error as exc:
            raise RuntimeError(f"Count query failed: {exc}") from exc

    # ─── UPDATE ──────────────────────────────────────────────────────────

    def update_reading(self, reading_id: int, **kwargs: Any) -> bool:
        """
        Update one or more columns of an existing reading.

        Only the columns listed in the schema are accepted; unknown keys
        are silently ignored.

        Returns:
            ``True`` if exactly one row was modified.
        """
        allowed_columns = {
            "timestamp",
            "ammonia_ppm",
            "nitrite_ppm",
            "nitrate_ppm",
            "ph",
            "temperature_c",
            "water_changed",
            "water_change_volume_pct",
            "notes",
        }
        fields = {k: v for k, v in kwargs.items() if k in allowed_columns}
        if not fields:
            return False

        set_clause = ", ".join(f"{col} = ?" for col in fields)
        values: list = list(fields.values()) + [reading_id]
        sql = f"UPDATE readings SET {set_clause} WHERE id = ?;"

        try:
            with self._cursor() as cur:
                cur.execute(sql, values)
                return cur.rowcount > 0
        except sqlite3.Error as exc:
            raise RuntimeError(
                f"Failed to update reading {reading_id}: {exc}"
            ) from exc

    # ─── DELETE ──────────────────────────────────────────────────────────

    def delete_reading(self, reading_id: int) -> bool:
        """
        Delete a reading by its primary key.

        Returns:
            ``True`` if a row was actually removed.
        """
        sql = "DELETE FROM readings WHERE id = ?;"
        try:
            with self._cursor() as cur:
                cur.execute(sql, (reading_id,))
                return cur.rowcount > 0
        except sqlite3.Error as exc:
            raise RuntimeError(
                f"Failed to delete reading {reading_id}: {exc}"
            ) from exc

    # ─── CSV Export / Import ─────────────────────────────────────────────

    def export_to_csv(self, filepath: str) -> int:
        """
        Write every reading to a CSV file.

        Args:
            filepath: Destination file path (created / overwritten).

        Returns:
            Number of rows written.
        """
        readings = self.get_all_readings()
        if not readings:
            return 0
        try:
            path = Path(filepath)
            with path.open("w", newline="", encoding="utf-8") as fh:
                writer = csv.DictWriter(fh, fieldnames=readings[0].keys())
                writer.writeheader()
                writer.writerows(readings)
            return len(readings)
        except OSError as exc:
            raise RuntimeError(f"CSV export failed: {exc}") from exc

    def import_from_csv(self, filepath: str) -> int:
        """
        Bulk-import readings from a CSV file.

        The CSV must contain at least the columns:
        ``ammonia_ppm``, ``nitrite_ppm``, ``nitrate_ppm``, ``ph``,
        ``temperature_c``.  Optional: ``water_changed``,
        ``water_change_volume_pct``, ``notes``, ``timestamp``.

        Args:
            filepath: Source CSV path.

        Returns:
            Number of rows imported.
        """
        try:
            path = Path(filepath)
            count = 0
            with path.open("r", encoding="utf-8") as fh:
                reader = csv.DictReader(fh)
                for row in reader:
                    self.insert_reading(
                        ammonia_ppm=float(row["ammonia_ppm"]),
                        nitrite_ppm=float(row["nitrite_ppm"]),
                        nitrate_ppm=float(row["nitrate_ppm"]),
                        ph=float(row["ph"]),
                        temperature_c=float(row["temperature_c"]),
                        water_changed=bool(int(row.get("water_changed", "0"))),
                        water_change_volume_pct=float(
                            row.get("water_change_volume_pct", "0.0")
                        ),
                        notes=row.get("notes", ""),
                        timestamp=row.get("timestamp"),
                    )
                    count += 1
            return count
        except (OSError, KeyError, ValueError) as exc:
            raise RuntimeError(f"CSV import failed: {exc}") from exc

    # ─── Aquarium Profile ────────────────────────────────────────────────

    def get_profile(self) -> Optional[Dict[str, Any]]:
        """Return the aquarium profile, or ``None`` if not yet created."""
        sql = "SELECT * FROM aquarium_profile WHERE id = 1;"
        try:
            with self._cursor() as cur:
                cur.execute(sql)
                row = cur.fetchone()
                return dict(row) if row else None
        except sqlite3.Error as exc:
            raise RuntimeError(f"Failed to fetch profile: {exc}") from exc

    def save_profile(
        self,
        tank_name: str,
        tank_size_liters: float,
        fish_species: str,
    ) -> None:
        """
        Create or update the single-row aquarium profile (upsert).

        Args:
            tank_name:        Display name for the aquarium.
            tank_size_liters: Tank volume in litres.
            fish_species:     Key from ``FISH_PROFILES``.
        """
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = """
            INSERT INTO aquarium_profile
                (id, tank_name, tank_size_liters, fish_species, created_at, updated_at)
            VALUES (1, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                tank_name        = excluded.tank_name,
                tank_size_liters = excluded.tank_size_liters,
                fish_species     = excluded.fish_species,
                updated_at       = excluded.updated_at;
        """
        try:
            with self._cursor() as cur:
                cur.execute(
                    sql, (tank_name, tank_size_liters, fish_species, now, now)
                )
        except sqlite3.Error as exc:
            raise RuntimeError(f"Failed to save profile: {exc}") from exc


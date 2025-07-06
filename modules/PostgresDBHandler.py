import pandas as pd
import psycopg2


class PostgresDBHandler:
    def __init__(self, dbname, user, password, host, port="5432"):
        self.conn_params = {
            "dbname": dbname,
            "user": user,
            "password": password,
            "host": host,
            "port": port,
        }
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(**self.conn_params)
            self.cursor = self.conn.cursor()
            # print("Connection established")
        except Exception as e:
            print(f"An error occurred while connecting to the database: {e}")

    def execute_query(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
        except Exception as e:
            print(f"An error occurred while executing the query: {e}")

    def fetchone(self):
        try:
            return self.cursor.fetchone()
        except Exception as e:
            print(f"An error occurred while fetching one result: {e}")

    def fetchall(self):
        try:
            return self.cursor.fetchall()
        except Exception as e:
            print(f"An error occurred while fetching all results: {e}")

    def close(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
            # print("Connection closed")
        except Exception as e:
            print(f"An error occurred while closing the connection: {e}")

    # Instruments
    def get_instrument_id(self, name):
        query = "SELECT instrumentID FROM Instruments WHERE name = %s"
        self.execute_query(query, (name,))
        result = self.fetchone()
        return result[0] if result else None

    def get_all_instruments(self):
        query = "SELECT name, audioCount FROM Instruments"
        self.execute_query(query)
        return [item[0] for item in self.fetchall()]

    def get_mappings_instruments(self):
        query = "SELECT instrumentid, name FROM Instruments ORDER BY instrumentid"
        self.execute_query(query)
        return pd.DataFrame(self.fetchall(), columns=["instrumentid", "name"])

    def get_count_instruments(self):
        query = "SELECT COUNT(*) FROM Instruments"
        self.execute_query(query)
        return self.fetchone()[0]

    def insert_instrument(self, name, audioCount):
        query = "INSERT INTO Instruments (name, audioCount) VALUES (%s, %s) RETURNING instrumentID"
        self.execute_query(query, (name, audioCount))
        return self.fetchone()[0]

    def increment_instrument_audioCount(self, instrument_id):
        query = (
            "UPDATE Instruments SET audioCount = audioCount + 1 WHERE instrumentID = %s"
        )
        self.execute_query(query, (instrument_id,))

    def decrement_instrument_audioCount(self, instrument_id):
        query = (
            "UPDATE Instruments SET audioCount = audioCount - 1 WHERE instrumentID = %s"
        )
        self.execute_query(query, (instrument_id,))

    # AudioFiles
    def insert_audio_file(self, filePath, sampleRate, duration, instrument_id):
        query = """
        INSERT INTO AudioFiles (filePath, sampleRate,duration, instrumentID)
        VALUES (%s, %s, %s, %s)
        RETURNING audioID
        """

        self.increment_instrument_audioCount(instrument_id)
        self.execute_query(query, (filePath, sampleRate, duration, instrument_id))
        return self.fetchone()[0]

    def get_all_audio_ids(self):
        query = "SELECT audioID FROM AudioFiles"
        self.execute_query(query)
        return [item[0] for item in self.fetchall()]

    def get_audio_file(self, audio_id):
        query = "SELECT audioID, filePath, instrumentID, sampleRate, duration FROM AudioFiles WHERE audioID = %s"
        self.execute_query(query, (audio_id,))
        result = self.fetchone()
        return {
            "audioID": result[0],
            "filePath": result[1],
            "instrumentID": result[2],
            "sampleRate": result[3],
            "duration": result[4],
        }

    def get_audio_files(self, audio_ids):
        query = "SELECT audioID, filePath, instrumentID, sampleRate, duration FROM AudioFiles WHERE audioID = ANY(%s)"
        self.execute_query(query, (audio_ids,))
        result = self.fetchall()

        return [
            {
                "audioID": row[0],
                "filePath": row[1],
                "instrumentID": row[2],
                "sampleRate": row[3],
                "duration": row[4],
            }
            for row in result
        ]

    def check_audio_file_exists(self, filePath):
        query = "SELECT audioID FROM AudioFiles WHERE filePath = %s"
        self.execute_query(query, (filePath,))
        return self.fetchone() is not None

    # Processed
    def insert_processed_audio(
        self,
        instrumentID,
        audioID,
        fixedLength,
        spectrogramPath,
        mfccPath,
        augmentation,
    ):
        query = """
        INSERT INTO Processed (instrumentID, audioID, fixedLength, spectrogramPath, mfccPath, augmentation)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING audioID
        """
        self.execute_query(
            query,
            (
                instrumentID,
                audioID,
                fixedLength,
                spectrogramPath,
                mfccPath,
                augmentation,
            ),
        )
        return self.fetchone()[0]

    def get_all_processed_ids(self):
        query = "SELECT processedID FROM Processed"
        self.execute_query(query)
        return [item[0] for item in self.fetchall()]

    def get_processed_fit_data(self, processedIDs):
        query = "SELECT processedID, spectrogramPath, mfccPath, instrumentID FROM Processed WHERE processedID = ANY(%s)"
        self.execute_query(query, (processedIDs,))
        return [
            {
                "processedID": item[0],
                "spectrogramPath": item[1],
                "mfccPath": item[2],
                "instrumentID": item[3],
            }
            for item in self.fetchall()
        ]

    def get_processed_audio(self, processedID):
        query = "SELECT processedID, instrumentID, audioID, fixedLength, spectrogramPath, mfccPath, augmentation FROM Processed WHERE processedID = %s"
        self.execute_query(query, (processedID,))
        result = self.fetchone()
        return {
            "processedID": result[0],
            "instrumentID": result[1],
            "audioID": result[2],
            "fixedLength": result[3],
            "spectrogramPath": result[4],
            "mfccPath": result[5],
            "augmentation": result[6],
        }

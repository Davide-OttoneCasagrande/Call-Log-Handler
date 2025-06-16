from pathlib import Path
import logging
import sys

import dataStore
import loader
import config

logger = logging.getLogger(__name__)
#logger.setLevel(logging.DEBUG)

def main(length_between_logging: int = 100) -> None:
    """
    Executes the log collection and export pipeline.

    Steps:
    1. Load configuration from the config file.
    2. Load call logs from the specified folder.
    3. Process each log and store it using the DataStore module
    4. Log progress every `length_between_logging` entries

    Args:
        length_between_logging (int): Number of logs to process before logging progress.
            Default is 100.

    Raises:
        SystemExit: If configuration loading or pipeline execution fails.
    """
    try:
        settings = config.Config()

        logger.info("Initializing log processing pipeline...")

        files = loader.CallLogLoader(settings["folder_path"])
        db = dataStore.DataStore(
            settings["export_path"], settings["elasticsearch_address"], settings["index_name"])

        if not db.index_exists:
            if settings["mapping"] is None:
                logger.warning(
                    "Mapping configuration is missing in the config file, index created empty.")
            db.create_mapping(settings["mapping"])
            logger.info(
                f"Index '{settings['index_name']}' doesn't exists, using config mapping.")

        logger.info("Starting log processing...")
        total_processed: int = process_logs(files, db, length_between_logging)

        success_message: str = f"Successfully processed {total_processed} logs"
        logger.info(success_message)
        print(success_message)

    except Exception as e:
        error_message: str = f"Pipeline failed: {e}"
        logger.error(error_message, exc_info=True)
        print(f"Error: {error_message}")
        sys.exit(1)


def process_logs(files: loader.CallLogLoader, db: dataStore.DataStore, batch_size: int) -> int:
    """
    Process and insert logs into the database.

    Args:
        files: CallLogLoader instance for reading CSV files
        db: DataStore instance for database operations
        batch_size: Number of logs to process before logging progress

    Returns:
        Total number of logs processed
    """
    logs_processed = 0
    batch_count = 0

    try:
        for row in files.load_csv_files():
            db.insert(row.to_json())
            logs_processed += 1

            if logs_processed % batch_size == 0:
                batch_count += 1
                logger.info(
                    f"Processed {logs_processed} logs (batch {batch_count} completed)")

    except Exception as e:
        logger.error(
            f"Error processing logs at entry {logs_processed + 1}: {e}")
        raise

    return logs_processed


if __name__ == "__main__":
    main()

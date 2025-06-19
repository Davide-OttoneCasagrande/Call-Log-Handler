from pathlib import Path
import logging
import sys

import dataStore
import loader
import config

log_path: str = "src/logs//app.log"
# Configuring root logger with proper formatting and handlers.
log_file = Path(log_path)
log_file.parent.mkdir(parents=True, exist_ok=True)

file_format = logging.Formatter("[%(levelname)s]%(asctime)s - %(name)s: %(message)s")
file_handler = logging.FileHandler(log_file)
file_handler.setFormatter(file_format)

stream_format = logging.Formatter("[%(levelname)s] - %(name)s: %(message)s")
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(stream_format)

logging.basicConfig(
    level=logging.INFO,
    #datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[file_handler, stream_handler]
)

# Set up module-level logger.
logger = logging.getLogger(__name__)
#logger.setLevel(logging.DEBUG)


def main(length_between_logging: int = 500) -> None:
    """
    Executes the log collection and export pipeline.

    Steps:
    1. Load configuration from the config file.
    2. Load call logs from the specified folder.
    3. Process each log and store it using the DataStore module
    4. Log progress every `length_between_logging` entries

    Args:
        length_between_logging (int): Number of logs to process before logging progress.
            Default is 500.

    Raises:
        SystemExit: If configuration loading or pipeline execution fails.
    """
    try:
        logger.info("initializing configuration settings...")
        configs= config.Config()

        logger.info("initalizing log processing pipeline...")

        files = loader.CallLogLoader(configs.folder_path)
        db = dataStore.DataStore(
            configs.export_path, configs.elasticsearch_address, configs.index_name)

        if configs.elasticsearch_address and not db.index_exists:
            if configs.mapping is not None:
                db.create_mapping(configs.mapping)
                logger.info(f"Index '{configs.index_name}' doesn't exists, using config mapping.")
            else:
                logger.warning("Mapping configuration is missing in the config file, index created empty.")

        logger.info("Starting log processing...")

        total_processed: int = process_logs(files, db, length_between_logging)

        success_message: str = f"Successfully processed {total_processed} logs"
        logger.info(success_message)

    except Exception as e:
        error_message: str = f"Pipeline failed: {e}"
        logger.critical(error_message, exc_info=True)
        sys.exit(1)


def process_logs(files: loader.CallLogLoader, db: dataStore.DataStore, batch_size: int) -> int:
    """
    Process and insert logs into the database.

    Args:
        files (CallLogLoader): Instance for reading CSV files.
        db (DataStore): Instance for database operations.
        batch_size (int): Number of logs to process before logging progress.

    Returns:
        Total number of logs processed

    Raises:
        Exception: If an error occurs during log processing.
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
        logger.critical(
            f"Error processing logs at entry {logs_processed + 1}: {e}", exc_info=True)
        raise

    return logs_processed

if __name__ == "__main__":
    main()

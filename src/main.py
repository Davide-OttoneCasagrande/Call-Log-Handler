from pathlib import Path
import logging
import sys

import dataStore
import loader


def setup_logging(log_path: str) -> None:
    """Configure logging with proper formatting and handlers."""
    log_file = Path(log_path)
    log_file.parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )


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
        config: dict = load_config()
        setup_logging(config["log_path"])

        logging.info("Initializing log processing pipeline...")

        files = loader.CallLogLoader(config["folder_path"])
        db = dataStore.DataStore(
            config["export_path"], config["elasticsearch_address"], config["index_name"])

        if not db.index_exists:
            if config["mapping"] is None:
                logging.warning(
                    "Mapping configuration is missing in the config file, index created empty.")
            db.create_mapping(config["mapping"])
            logging.info(
                f"Index '{config['index_name']}' doesn't exists, using config mapping.")

        logging.info("Starting log processing...")
        total_processed: int = process_logs(files, db, length_between_logging)

        success_message: str = f"Successfully processed {total_processed} logs"
        logging.info(success_message)
        print(success_message)

    except Exception as e:
        error_message: str = f"Pipeline failed: {e}"
        logging.error(error_message, exc_info=True)
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
                logging.info(
                    f"Processed {logs_processed} logs (batch {batch_count} completed)")

    except Exception as e:
        logging.error(
            f"Error processing logs at entry {logs_processed + 1}: {e}")
        raise

    return logs_processed


if __name__ == "__main__":
    main()

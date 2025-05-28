import logCollector
from src_logs_Generator import logCSVGen as fileGen

def main(num_entries: int = None, file_path: str = None):
    """
    Main function to demonstrate the usage of LogCollector and file generation.

    Args:
        num_entries (int, optional): Number of log entries to generate.
        file_path (str, optional): Path to the log file.
    """
    
    print("Generating random log file...")
    fileGen.gererate_random_logFile(num_entries)    # Generate a sample log CSV file
    print("Collecting logs from the generated file...")
    logCollector.logCollector(file_path)   # Collect the logs from the generated file
    print("Log collection completed successfully.")

if __name__ == "__main__":
    main()
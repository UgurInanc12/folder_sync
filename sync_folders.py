import os
import shutil
import argparse
import logging
import time
import hashlib

def calculate_md5(file_path, chunk_size=4096):
    """
    This function calculates the MD5 hash of a file.
    It helps to check if two files are the same.
    """
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                hash_md5.update(chunk)
    except Exception as e:
        logging.error(f"Error reading file {file_path}: {e}")
        return None
    return hash_md5.hexdigest()

def sync_folders(source, replica):
    """
    This function makes the replica folder exactly the same as the source folder.
    
    It copies new and updated files from source to replica.
    Then it deletes files in replica that are not in source.
    """
    # Copy or update files from source to replica
    for dirpath, dirnames, filenames in os.walk(source):
        # Create relative path for the current folder
        rel_path = os.path.relpath(dirpath, source)
        replica_dir = os.path.join(replica, rel_path)
        
        # Make replica folder if it does not exist
        if not os.path.exists(replica_dir):
            os.makedirs(replica_dir)
            logging.info(f"Created folder: {replica_dir}")
        
        # For each file in the current folder
        for file in filenames:
            source_file = os.path.join(dirpath, file)
            replica_file = os.path.join(replica_dir, file)
            
            # If file does not exist in replica, copy it
            if not os.path.exists(replica_file):
                try:
                    shutil.copy2(source_file, replica_file)
                    logging.info(f"Copied file: {source_file} --> {replica_file}")
                except Exception as e:
                    logging.error(f"Error copying {source_file} to {replica_file}: {e}")
            else:
                # Check if the file is different using MD5 hash
                source_md5 = calculate_md5(source_file)
                replica_md5 = calculate_md5(replica_file)
                if source_md5 != replica_md5:
                    try:
                        shutil.copy2(source_file, replica_file)
                        logging.info(f"Updated file: {source_file} --> {replica_file}")
                    except Exception as e:
                        logging.error(f"Error updating {source_file} to {replica_file}: {e}")

    # Remove files and folders from replica that are not in source
    for dirpath, dirnames, filenames in os.walk(replica, topdown=False):
        rel_path = os.path.relpath(dirpath, replica)
        source_dir = os.path.join(source, rel_path)

        # Delete files not in source
        for file in filenames:
            replica_file = os.path.join(dirpath, file)
            source_file = os.path.join(source_dir, file)
            if not os.path.exists(source_file):
                try:
                    os.remove(replica_file)
                    logging.info(f"Deleted file: {replica_file}")
                except Exception as e:
                    logging.error(f"Error deleting file {replica_file}: {e}")
        
        # Delete folder if it does not exist in source
        if not os.path.exists(source_dir):
            try:
                shutil.rmtree(dirpath)
                logging.info(f"Deleted folder: {dirpath}")
            except Exception as e:
                logging.error(f"Error deleting folder {dirpath}: {e}")

def setup_logging(log_file):
    """
    This function sets up logging to show messages on the screen and in a file.
    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Handler for console
    c_handler = logging.StreamHandler()
    # Handler for file
    f_handler = logging.FileHandler(log_file)
    c_handler.setLevel(logging.INFO)
    f_handler.setLevel(logging.INFO)

    # Create a simple format for the logs
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(formatter)
    f_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

def main():
    # Define command line arguments using argparse
    parser = argparse.ArgumentParser(description='Synchronize two folders.')
    parser.add_argument('--source', type=str, required=True, help='Path to the source folder')
    parser.add_argument('--replica', type=str, required=True, help='Path to the replica folder')
    parser.add_argument('--interval', type=int, required=True, help='Synchronization interval in seconds')
    parser.add_argument('--log', type=str, required=True, help='Path to the log file')
    args = parser.parse_args()
    
    # Create source and replica folders if they do not exist
    if not os.path.exists(args.source):
        os.makedirs(args.source)
        print(f"Created source folder: {args.source}")
    if not os.path.exists(args.replica):
        os.makedirs(args.replica)
        print(f"Created replica folder: {args.replica}")

    # Setup logging with the given log file
    setup_logging(args.log)
    logging.info("Starting folder synchronization...")
    logging.info(f"Source folder: {args.source}")
    logging.info(f"Replica folder: {args.replica}")
    logging.info(f"Synchronization interval: {args.interval} seconds")
    
    # Run sync in a loop with the given interval
    try:
        while True:
            logging.info("Starting a new synchronization cycle...")
            sync_folders(args.source, args.replica)
            logging.info("Cycle complete. Waiting for next cycle...")
            time.sleep(args.interval)
    except KeyboardInterrupt:
        logging.info("Synchronization stopped by user.")

if __name__ == "__main__":
    main()

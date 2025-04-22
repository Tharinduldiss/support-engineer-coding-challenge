import csv
import requests

API_URL = "https://example.com/api/create_user"
ERROR_LOG_FILE = "error_log.txt"
REQUIRED_FIELDS = ["email"]


def is_valid_row(row):
    """Check if all required fields are present and not empty."""
    return all(row.get(field) for field in REQUIRED_FIELDS)


def log_error(row, error_message):
    """Log errors to a file."""
    with open(ERROR_LOG_FILE, "a") as log_file:
        log_file.write(f"Failed to create user {row.get('email', 'N/A')}: {error_message}\n")


def create_user(row):
    """Send a POST request to create a user and handle errors."""
    try:
        response = requests.post(API_URL, json=row)
        if response.status_code != 201:
            log_error(row, f"Status Code: {response.status_code}, Response: {response.text}")
    except requests.exceptions.RequestException as e:
        log_error(row, str(e))


def create_users_from_csv(file_path):
    """Main function to read CSV and create users."""
    with open(file_path, mode='r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if is_valid_row(row):
                create_user(row)
            else:
                log_error(row, "Missing required fields")


if __name__ == "__main__":
    create_users_from_csv("users.csv")

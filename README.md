# Media Service

A FastAPI-based service for managing media files with S3 integration.

## Features
- Upload files to S3 and local storage.
- Retrieve files from local storage or S3.
- Database integration with PostgreSQL.

## Setup

### Prerequisites
- Docker and Docker Compose.
- Python 3.11.

### Environment Variables
Create a `.env` file based on `.env.example` and provide values for:
- PostgreSQL credentials.
- AWS S3 credentials.

### Build and Run
1. Build and start the service:
   ```bash
   docker-compose up --build

### Clear Disk Script
The `clear_disk.sh` script is used to clean old files from the `media` directory. 

#### Setup
1. Specify the path to the directory where old files will be deleted in the `clear_disk.sh` file

2. Make sure the script is executable:
   ```bash
   chmod +x clear_disk.sh

3. Add the script to the system's crontab to run periodically

4. Open the crontab editor:
   ```bash
   crontab -e
   ```

5. Add the following line to execute the script every hour (as an example):
   ```bash
   0 * * * * /full/path/to/clear_disk.sh
   ```
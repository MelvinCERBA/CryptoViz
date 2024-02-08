#!/bin/bash

# Set the backup directory
BACKUP_DIR="/grafana/backups"

# Specify the backup filename to restore
# Ensure to replace this with the actual filename you want to restore
BACKUP_FILENAME="grafana_backup.tar.gz"

# Path to the backup file
BACKUP_PATH="$BACKUP_DIR/$BACKUP_FILENAME"

# Volume name to restore to
VOLUME_NAME="grafana_grafana-data"

# Check if the backup file exists
if [ ! -f "$BACKUP_PATH" ]; then
    echo "Backup file does not exist: $BACKUP_PATH"
    exit 1
fi

# Restore the backup to the specified Docker volume
docker run --rm -v $VOLUME_NAME:/grafana-data -v $BACKUP_DIR:/backup busybox tar xzf /backup/$BACKUP_FILENAME -C /grafana-data

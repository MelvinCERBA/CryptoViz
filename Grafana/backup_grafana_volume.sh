#!/bin/bash

# Set the backup directory
BACKUP_DIR="/grafana/backups"

# Volume name to backup
VOLUME_NAME="grafana_grafana-data"

# Backup filename - constant, does not include date
BACKUP_FILENAME="grafana_backup.tar.gz"

# Path to save the backup file
BACKUP_PATH="$BACKUP_DIR/$BACKUP_FILENAME"

# Ensure the backup directory exists
mkdir -p "$BACKUP_DIR"

# Run a container to backup the volume
docker run --rm -v $VOLUME_NAME:/volume -v $BACKUP_DIR:/backup ubuntu tar czf /backup/$BACKUP_FILENAME -C /volume ./

echo "Backup of $VOLUME_NAME completed: $BACKUP_PATH"

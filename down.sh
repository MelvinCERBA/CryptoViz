# Array of specific directories with Docker Compose projects, in the order they should be started
declare -a dirs=("_Infra/confluent" "_Infra/db" "API/" "Scrapper/" "SparksApp/" "WebApp/")

# Start Docker Compose projects in specified directories
for dir in "${dirs[@]}"; do
    if [ -f "$dir/docker-compose.yml" ]; then
        echo "Stopping Docker Compose project in $dir"
        (cd "$dir" && docker-compose down)
    else
        echo "No docker-compose.yml found in $dir. Skipping..."
    fi
done
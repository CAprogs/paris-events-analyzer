default:
    @just --list --list-prefix " ➫ " --unsorted

set dotenv-load

STACK_NAME := "paris-event-analyzer"

# Docker

# Check the docker compose file consistency
comp-check:
    @echo "\nChecking docker-compose consistency ..\n"
    @docker compose config --no-interpolate

# Start the docker compose stack
comp-start: comp-check
    @echo "\nCreating the datalake directory if it does not exist .."
    @mkdir -p datalake/
    @sleep 2
    @echo "\nStarting {{STACK_NAME}} stack..\n"
    @docker compose up -d

# Restart the docker compose stack
comp-restart:
    @echo "\nRestarting {{STACK_NAME}} stack ..\n"
    @docker compose restart {{STACK_NAME}}

# Stop the docker compose stack and remove containers
comp-clean:
    @echo "\nStopping {{STACK_NAME}} stack ..\n"
    @docker compose down

# Show all docker compose stack
comp-show:
    @echo "\nShowing docker-compose stack ..\n"
    @docker compose ps -a

# Start the ingestion
start:
    @echo "\nStarting the ingestion ..\n"
    @uv run src/ingestion/main.py
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

# Pre-commit

# Run pre-commit checks and update hooks if possible
quality:
	@echo "Checking pre-commit config consistency"
	@uv run pre-commit validate-config
	@echo "\nInstalling pre-commit hooks\n"
	@uv run pre-commit install --install-hooks
	@echo "\nChecking for hook updates\n"
	@uv run pre-commit autoupdate

# Run pre-commit checks and hooks on modified files only
quality-default: quality
	@echo "\nRunning pre-commit on staged files\n"
	@uv run pre-commit run

# Run pre-commit checks and hooks on a all project files
quality-all: quality
	@echo "\nRunning pre-commit on all files\n"
	@uv run pre-commit run --all-files
-   repo: https://github.com/commitizen-tools/commitizen
    rev: v3.27.0 # Utilisez la version la plus récente
    hooks:
    -   id: commitizen

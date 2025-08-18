[private]
default:
    @just --list --list-prefix " ➫ " --unsorted

set dotenv-load

STACK_NAME := "paris-event-analyzer"
DATABASE_PATH := "warehouse/prod.duckdb"
INGESTION_ENTRYPOINT := "src/ingestion/main.py"
WEB_APP_ENTRYPOINT := "app.py"

# Docker

# Check the docker compose file consistency
[group("docker")]
comp-check:
    @echo "\nChecking docker-compose consistency ..\n"
    @docker compose config --no-interpolate

# Start the docker compose stack
[group("docker")]
comp-start: comp-check
    @echo "\nCreating the datalake directory if it does not exist .."
    @mkdir -p datalake/
    @sleep 2
    @echo "\nStarting {{STACK_NAME}} stack..\n"
    @docker compose up -d

# Restart the docker compose stack
[group("docker")]
comp-restart:
    @echo "\nRestarting {{STACK_NAME}} stack ..\n"
    @docker compose restart {{STACK_NAME}}

# Stop the docker compose stack and remove containers
[group("docker")]
comp-clean:
    @echo "\nStopping {{STACK_NAME}} stack ..\n"
    @docker compose down

# Show all docker compose stack
[group("docker")]
comp-show:
    @echo "\nShowing docker-compose stack ..\n"
    @docker compose ps -a

# Pre-commit

# Run pre-commit checks and update hooks if possible
[group("test")]
quality:
	@echo "Checking pre-commit config consistency"
	@uv run pre-commit validate-config
	@echo "\nInstalling pre-commit hooks\n"
	@uv run pre-commit install --install-hooks
	@echo "\nChecking for hook updates\n"
	@uv run pre-commit autoupdate

# Run pre-commit checks and hooks on modified files only
[group("test")]
quality-default: quality
	@echo "\nRunning pre-commit on staged files\n"
	@uv run pre-commit run

# Run pre-commit checks and hooks on a all project files
[group("test")]
quality-all: quality
	@echo "\nRunning pre-commit on all files\n"
	@uv run pre-commit run --all-files

# DBT

# Debug the dbt project configuration
[group("dbt")]
dbt-debug:
    @echo "\nDebugging profile config .."
    @uv run dbt debug --config-dir
    @uv run dbt debug

# Build and serve the dbt documentation
[group("dbt")]
dbt-catalog: dbt-debug
    @echo "\nBuilding catalog .."
    @dbt docs generate
    @echo "\nOpening DBT documentation .."
    @dbt docs serve --port 3000

# Run the dbt project
[group("dbt")]
dbt-run: dbt-debug
    @echo "\nRunning dbt models .."
    @uv run dbt run

# Clean the dbt project by removing compiled file, artifacts and logs
[group("dbt")]
dbt-clean: dbt-debug
    @echo "\nCleaning dbt project .."
    @uv run dbt clean --no-clean-project-files-only

# Start the DuckDB UI after running dbt models
[group("dbt")]
duckdb-ui: dbt-run
    @echo "\nStarting DuckDB UI .."
    @duckdb -ui {{DATABASE_PATH}}


# Final Workflow

# Run the ingestion workflow
[group("workflow")]
ingest:
		@uv run python {{INGESTION_ENTRYPOINT}}

# Run the exposition workflow
[group("workflow")]
expose:
		@uv run streamlit run {{WEB_APP_ENTRYPOINT}}

# Run the entire workflow process, from ingestion to exposition
[group("workflow")]
final-workflow: ingest dbt-run expose

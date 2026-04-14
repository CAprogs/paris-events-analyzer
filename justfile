# .. previous content

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
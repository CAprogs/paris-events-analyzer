# ==================================================================================== #
#                       Fichier d'automatisation pour le projet
#                    Utilisation : 'just <nom_de_la_recette>'
# ==================================================================================== #

# Configuration par défaut pour lister les commandes disponibles avec 'just'
default:
    @just --list --list-prefix " ➫ " --unsorted

# Charge les variables d'environnement si un fichier .env existe
set dotenv-load

# --- Variables de configuration ---
STACK_NAME := "paris-event-analyzer"

# --- Gestion de Docker ---

# Vérifie la cohérence du fichier docker-compose
comp-check:
    @echo "\nChecking docker-compose consistency ..\n"
    @docker compose config --no-interpolate

# Démarre la stack Docker
comp-start: comp-check
    @echo "\nCreating the datalake directory if it does not exist .."
    @mkdir -p datalake/
    @sleep 2
    @echo "\nStarting {{STACK_NAME}} stack..\n"
    @docker compose up -d

# Redémarre la stack Docker
comp-restart:
    @echo "\nRestarting {{STACK_NAME}} stack ..\n"
    @docker compose restart

# Arrête la stack Docker et supprime les conteneurs
comp-clean:
    @echo "\nStopping {{STACK_NAME}} stack ..\n"
    @docker compose down

# Affiche les conteneurs de la stack
comp-show:
    @echo "\nShowing docker-compose stack ..\n"
    @docker compose ps -a

# --- Pre-commit (Qualité du code) ---
# Tâche de base : valide la config, installe et met à jour les hooks
quality:
    @echo "Checking pre-commit config consistency"
    @uv run pre-commit validate-config
    @echo "\nInstalling pre-commit hooks\n"
    @uv run pre-commit install --install-hooks
    @echo "\nChecking for hook updates\n"
    @uv run pre-commit autoupdate

# Lance les hooks sur les fichiers modifiés et "staged" (pour un commit)
quality-default: quality
    @echo "\nRunning pre-commit on staged files\n"
    @uv run pre-commit run

# Lance les hooks sur TOUS les fichiers du projet
quality-all: quality
    @echo "\nRunning pre-commit on all files\n"
    @uv run pre-commit run --all-files
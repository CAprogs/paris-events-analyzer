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

# --- Mise en place, Lancement et Qualité ---

# Installe les dépendances ET configure les pre-commit hooks
setup: pre-commit-setup
    @echo "\n Mise en place de l'environnement et installation des dépendances..."
    @uv sync --dev

# Installe les pre-commit hooks pour le dépôt
pre-commit-setup:
    @echo "\n Installation des pre-commit hooks..."
    @uv run pre-commit install

# Lance le script d'ingestion des données
# !!! MODIFIEZ 'path/to/your/ingestion_script.py' avec le vrai chemin de votre script !!!
ingest:
    @echo " Lancement du script d'ingestion des données..."
    @uv run python path/to/your/ingestion_script.py

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


# --- Gestion de Docker ---

# Vérifie la cohérence du fichier docker-compose
comp-check:
    @echo "\n Vérification de la cohérence de docker-compose...\n"
    @docker compose config --no-interpolate

# Démarre la stack Docker
comp-start: comp-check
    @echo "\n Création du dossier datalake s'il n'existe pas..."
    @mkdir -p datalake/
    @sleep 2
    @echo "\n Démarrage de la stack {{STACK_NAME}}...\n"
    @docker compose up -d

# Redémarre la stack Docker
comp-restart:
    @echo "\n Redémarrage de la stack {{STACK_NAME}}...\n"
    @docker compose restart

# Arrête la stack Docker et supprime les conteneurs
comp-clean:
    @echo "\n Arrêt de la stack {{STACK_NAME}}...\n"
    @docker compose down

# Affiche les conteneurs de la stack
comp-show:
    @echo "\n Affichage de la stack docker-compose...\n"
    @docker compose ps -a
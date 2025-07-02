from src.exposition.tables import Table
from src.exposition.main import serve
import dotenv

# Load environment variables from a .envrc file
dotenv.load_dotenv()

tables = [
    Table(database="warehouse/prod.duckdb", schema="gold", name="today_events"),
    Table(database="warehouse/prod.duckdb", schema="gold", name="nb_events_by_tags"),
]
# run the streamlit app
serve(tables=tables)

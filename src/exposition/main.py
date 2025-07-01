import streamlit as st
from exposition.tables import Table
from pandas import DataFrame
from streamlit.runtime.media_file_storage import MediaFileStorageError
import pendulum


def serve(tables: list[Table]) -> None:
    st.set_page_config(page_title="Paris Events Analyzer", page_icon="📆", layout="wide", initial_sidebar_state="auto")

    # Since the page config should be set before any other Streamlit commands
    from exposition.utils import fetch_data

    # Initialize session state variables if they do not exist
    if "selected_event_id" not in st.session_state:
        st.session_state["selected_event_id"] = None

    if "event_details" not in st.session_state:
        st.session_state["event_details"] = {
            "event_id": "",
            "cover_url": "",
            "description": "",
            "nb_next_occurrences": 0,
            "price_detail": "",
            "date_end": "",
            "next_start_date": "",
            "full_address": "",
            "ticket_resa_and_more_url": "",
            "contact_phone": "",
            "latitude": None,
            "longitude": None,
        }

    _, top_middle, _ = st.columns([3.5, 4, 2])

    with top_middle:
        st.title(":rainbow[Today's] Paris Events", anchor=False)
        _, info_col, _ = st.columns([2.5, 8, 1.5], vertical_alignment="center")
        with info_col:
            st.markdown(":small[Powered by] :blue-badge[**DataNova**]")
        st.divider(width=410)

    # Data Loading
    data = fetch_data(tables=tables)
    df: DataFrame = data.get("today_events", DataFrame())
    df_events_tag: DataFrame = data.get("nb_events_by_tags", DataFrame())

    # Use a copy of the original dataframe for filtering
    filtered_df = df.copy()

    # --> SIDEBAR SECTION
    st.sidebar.header("⚙️ Filtres")

    # Price type filter
    price_types = ["Tous"] + sorted(df["price_type"].dropna().unique().tolist())
    selected_price_type = st.sidebar.selectbox("💰 Type de prix", price_types, key="price_type_filter")

    # Event Category filter
    qfap_tags = ["Tous"] + sorted(df_events_tag["qfap_tags_distinct"].tolist())
    selected_category = st.sidebar.selectbox("🏷️ Catégorie", qfap_tags, key="qfap_tags_filter")

    # Accessibility filter
    handicap_options = ["Tous", "Accessible", "Non accessible"]
    selected_handicap = st.sidebar.selectbox("♿ Accessibilité", handicap_options, key="handicap_filter")

    # Zipcode filter
    zipcodes = ["Tous"] + sorted(df["address_zipcode"].dropna().astype(str).unique().tolist())
    selected_zipcode = st.sidebar.selectbox("📍 Code postal", zipcodes, key="zipcode_filter")

    if selected_price_type != "Tous":
        filtered_df = filtered_df[filtered_df["price_type"] == selected_price_type]

    if selected_category != "Tous":
        filtered_df = filtered_df[filtered_df["qfap_tags"].str.contains(selected_category, na=False)]

    if selected_handicap != "Tous":
        if selected_handicap == "Accessible":
            filtered_df = filtered_df[filtered_df["is_handicap_friendly"] == True]  # noqa: E712
        else:
            filtered_df = filtered_df[filtered_df["is_handicap_friendly"] == False]  # noqa: E712

    if selected_zipcode != "Tous":
        filtered_df = filtered_df[filtered_df["address_zipcode"].astype(str) == selected_zipcode]

    # --> STATISTICS SECTION
    st.subheader("📊 Statistiques")

    stats_col1, stats_col2, stats_col3 = st.columns(3)

    with stats_col1:
        st.metric("Nb événements", len(filtered_df))

    with stats_col2:
        accessible_count = len(filtered_df[filtered_df["is_handicap_friendly"] == True])  # noqa: E712
        st.metric("Avec accessibilité ♿", accessible_count)

    with stats_col3:
        with_location = len(filtered_df[filtered_df["latitude"].notna() & filtered_df["longitude"].notna()])
        st.metric("Avec localisation 📍", with_location)

    col1, _ = st.columns((2, 2))

    with col1:
        dropdown = st.expander("Autres statistiques", expanded=False)
        with dropdown:
            st.bar_chart(
                data={
                    "Gratuits 🐀": [len(filtered_df[filtered_df["price_type"] == "gratuit"])],
                    "Payants 💰": [len(filtered_df[filtered_df["price_type"] == "payant"])],
                    "Sous conditions 🤔": [len(filtered_df[filtered_df["price_type"] == "gratuit sous condition"])],
                },
                x_label="Nombre d'événements",
                horizontal=True,
                stack=False,
            )

    # --> MAIN CONTENT SECTION
    col1, col2 = st.columns([1.5, 2], gap="large")

    with col1:
        # Event list section
        st.subheader("📋 Liste des événements")

        # Columns to display in the dataframe
        display_columns = [
            "event_id",
            "title",
            "address_name",
            "address_zipcode",
            "is_handicap_friendly",
            "handicap_friendly_details",
        ]

        # Filter columns that exist in the dataframe
        available_columns = [col for col in display_columns if col in filtered_df.columns]

        if not filtered_df.empty:
            # Reset index to ensure proper row selection after filtering
            filtered_df = filtered_df.reset_index(drop=True)
            
            # --> DATAFRAME SECTION
            df_widget = st.dataframe(
                filtered_df[available_columns], use_container_width=True, on_select="rerun", selection_mode="single-row"
            )

            if df_widget.selection["rows"]:
                selected_index = df_widget.selection["rows"][0]
                # Use iloc for positional indexing on the reset dataframe
                st.session_state["event_details"] = {
                    k: filtered_df.iloc[selected_index][k]
                    for k, _ in st.session_state["event_details"].items()
                    if k in filtered_df.columns
                }

        else:
            st.info("Malheureusement, aucun événement n'a été trouvé ☹️")

        st.subheader("🗺️ Carte")

        # --> MAP SECTION
        not_null_location = filtered_df[filtered_df["latitude"].notna() & filtered_df["longitude"].notna()]

        if not not_null_location.empty and not df_widget.selection["rows"]:
            st.map(not_null_location, use_container_width=True)
        elif not not_null_location.empty and df_widget.selection["rows"]:
            lat = st.session_state["event_details"]["latitude"]
            lon = st.session_state["event_details"]["longitude"]
            df_lat_lon = DataFrame({"lat": [lat], "lon": [lon]})
            if df_lat_lon.isna().all().all():
                st.info("Aucune localisation disponible pour cet événement.")
            else:
                st.map(df_lat_lon, use_container_width=True)
        else:
            st.info("Impossible de localiser les événements 😵")

    # --> EVENT DETAILS SECTION
    with col2:
        st.subheader(":material/chat_info: Détails de l'événement")

        if not filtered_df.empty:
            if df_widget.selection["rows"]:
                try:
                    st.image(st.session_state["event_details"]["cover_url"], width=600)
                except MediaFileStorageError:
                    st.info("🖼️ Image non disponible")

                info_widgets = [
                    ("Description", "description"),
                    ("Adresse", "full_address"),
                    ("Nombre d'occurrences", "nb_next_occurrences"),
                    ("Détails prix", "price_detail"),
                    ("Date de fin", "date_end"),
                    ("Réservation / Billetterie", "ticket_resa_and_more_url"),
                    ("Contact", "contact_phone"),
                ]

                for label, field in info_widgets:
                    value = st.session_state["event_details"].get(field, None)

                    if field == "ticket_resa_and_more_url":
                        if value:
                            st.markdown(f"**{label}** : [🔗 Lien ]({value})")
                        else:
                            st.markdown(f"**{label}** : {value}")
                    elif field == "date_end":
                        formatted_date = pendulum.instance(value.to_pydatetime()).format(
                            "dddd DD MMMM YYYY", locale="fr"
                        )
                        st.markdown(f"**{label}** : {formatted_date}")
                    elif field == "description" or field == "price_detail":
                        st.markdown(f"**{label}** : {value}", unsafe_allow_html=True)
                    else:
                        st.markdown(f"**{label}** : {value}")
            else:
                st.info("💡 Sélectionnez un événement pour accéder aux détails.")
        else:
            st.info("Rien à voir ici 😶‍🌫️")

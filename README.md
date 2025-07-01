
<div align="center">

<img src="images/datanova-logo.png" alt="logo" width="500" height="160">



![GitHub](https://img.shields.io/github/license/CAprogs/paris-events-analyzer?color=blue)


# PARIS EVENTS ANALYZER

</div>


## À propos

Ce projet est la propriété de **DataNova**, startup spécialisée dans l'analyse de données Open-Source.

L'objectif principal de ce projet est de mettre en valeur les données ouvertes fournies par la ville de Paris pour analyser les événements culturels, sportifs et communautaires.

Vous retrouverez davantage d'informations sur les données ici : [Que Faire à Paris](https://opendata.paris.fr/explore/dataset/que-faire-a-paris-/).


### Architecture du projet

<img src="images/project-archi.png" alt="archi" width="1200" height="120">


<details>
    <summary>En savoir plus</summary>

Pourquoi ce choix ?
- **[Open Data Paris - API](https://opendata.paris.fr/pages/home/)** : Fournit des endpoints pour de nombreux jeux de données, notamment les événements de la ville de Paris.
- **[request-cache](https://requests-cache.readthedocs.io/en/stable/)** : C'est la bibliothèque request mais avec un cache intégré, ce qui permet de réduire les appels API inutiles et de rapidement itérer sur les données.
- **[MinIO x Docker](https://min.io/docs/minio/container/index.html)** : Self-hosted et scalable, MinIO est un `object storage` au même titre qu'Amazon S3, Google Cloud Storage ou Azure Blob Storage. Il permet de stocker les données de manière sécurisée et scalable. La seule différence est que, qui dit self-hosted dit gestion de la maintenance, des mises à jour et de la sécurité etc..
- **[DBT](https://docs.getdbt.com/docs/introduction)** : Facilite la transformation des données avec une approche modulaire et testable.
- **[DuckDB](https://duckdb.org/why_duckdb)** : Base de données légère et rapide, parfaite pour l'analyse de données.
- **[Streamlit](https://docs.streamlit.io/)** : Permet de créer rapidement des applications web interactives pour visualiser les données.
</details>


### À propos de "QUE FAIRE À PARIS" 💡
---

**QUE FAIRE À PARIS** est l’agenda participatif de la Ville de Paris. Tous les événements et activités de Paris et sa région sont publiés et mis en avant sur [ce site](https://www.paris.fr/quefaire).

👉 Les données recensées comprennent des informations sur les lieux parisiens tels que les **Bibliothèques** et **Musées** de la Ville, les **parcs** et **jardins**, les **centres d'animations**, les **piscines**, les **théâtres**, les **grands lieux** comme la **Gaîté Lyrique**, le **CENTQUATRE**, le **Carreau du Temple**, les **salles de concert**.

👉 Elles sont mises à jour **quotidiennement**.


### Description des données

<details>
    <summary> Data Model </summary>

| Feature | Description | Type | Exemple |
| :--- | :--- | :--- | :--- |
| `id` | Identifiant unique de l'événement. | VARCHAR | `315268` |
| `event_id` | Identifiant du modèle de l'événement (utilisé par Algolia). | INTEGER | `12345` |
| `url` | URL de la page de l'événement sur le site Que Faire à Paris. | VARCHAR | `https://quefaire.paris.fr/fiche/315268-le-bel-ete-du-canal` |
| `title` | Titre de l'événement. | VARCHAR | `Le Bel Été du Canal 2025` |
| `lead_text` | Texte d'introduction ou chapô de l'événement. | VARCHAR | `Chaque été, le canal de l'Ourcq s'anime ! Profitez de nombreuses animations, concerts et activités nautiques.` |
| `description` | Contenu détaillé de la fiche de l'événement, au format HTML. | VARCHAR | `<p>Rejoignez-nous pour la 18ème édition du Bel Été du Canal...</p>` |
| `date_start` | Date et heure de début de l'événement. | TIMESTAMPTZ | `2025-07-05T10:00:00+02:00` |
| `date_end` | Date et heure de fin de l'événement. | TIMESTAMPTZ | `2025-08-24T22:00:00+02:00` |
| `occurrences` | Dates et heures des différentes occurrences de l'événement. | VARCHAR | `2025-09-12T02:00:00+02:00_2025-09-12T02:00:00+02:00` |
| `date_description`| Description textuelle (HTML) des dates et horaires. | VARCHAR | `<p>Tous les samedis et dimanches du 5 juillet au 24 août 2025.</p>` |
| `cover_url` | URL de l'image de couverture de l'événement. | VARCHAR | `https://cdn.paris.fr/qfapv4/2024/08/05/huge-a33455995aae764b4149f08f72b37712.jpg` |
| `cover_alt` | Texte alternatif pour l'image de couverture. | VARCHAR | `Personnes faisant du kayak sur le canal de l'Ourcq` |
| `cover_credit` | Crédits de l'image de couverture. | VARCHAR | `© Mairie de Paris` |
| `locations` | Informations sur le lieu associé à l'événement. | VARCHAR | `[{"accessibility": {"blind": null, "pmr": 1, "deaf": null, "sign_language": null, "mental": null}, "address_street": ...}]` |
| `address_name` | Nom du lieu principal de l'événement. | VARCHAR | `Bassin de la Villette` |
| `address_street`| Adresse postale du lieu (numéro et rue). | VARCHAR | `Quai de la Loire` |
| `address_zipcode`| Code postal du lieu. | VARCHAR | `75019` |
| `address_city` | Ville du lieu. | VARCHAR | `Paris` |
| `lat_lon` | Coordonnées géographiques de l'événement. | GEOMETRY | `\x00\x00\x00\x00\x00\x00\x00\x00\x00...` |
| `pmr` | Indique si l'événement est accessible aux Personnes à Mobilité Réduite. | INTEGER | `1 / 0` |
| `blind` | Indique si l'événement est accessible aux personnes malvoyantes. | INTEGER | `1 / 0` |
| `deaf` | Indique si l'événement est accessible aux personnes malentendantes. | INTEGER | `1 / 0` |
| `sign_language` | Indique si l'accès en langue des signes est disponible. | VARCHAR | `1 / 0` |
| `mental` | Indique si l'accès est adapté pour les personnes en situation de handicap mental. | VARCHAR | `1 / 0` |
| `transport` | Moyens de transport pour accéder au lieu. | VARCHAR | `Métro 5 -> Jaurès, RER E : Magenta` |
| `contact_url` | URL du site web officiel ou de contact. | VARCHAR | `https://www.bel-ete-canal.fr` |
| `contact_phone` | Numéro de téléphone de contact. | VARCHAR | `01 42 76 33 50` |
| `contact_mail` | Adresse e-mail de contact. | VARCHAR | `contact@bel-ete-canal.fr` |
| `contact_facebook`| URL de la page Facebook de l'événement. | VARCHAR | `https://facebook.com/bel.ete.canal` |
| `contact_twitter`| URL du compte Twitter de l'événement. | VARCHAR | `https://twitter.com/bel_ete_canal` |
| `price_type` | Type de tarification de l'événement. | VARCHAR | `gratuit / payant / gratuit sous condition` |
| `price_detail` | Détails sur les tarifs. | VARCHAR | `<p>De 13 à 15 euros.</p>` |
| `access_type` | Type d'accès (libre, sur réservation...). | VARCHAR | `libre / conseillee` |
| `access_link` | URL pour la réservation ou l'achat de billets. | VARCHAR | `https://billetterie.bel-ete-canal.fr` |
| `access_link_text`| Texte du lien de réservation. | VARCHAR | `Réservez votre place ici` |
| `updated_at` | Date et heure de la dernière mise à jour de la fiche de l'événement. | TIMESTAMPTZ | `2025-06-12T15:00:00+02:00` |
| `image_couverture`| Champ technique lié à l'image de couverture. | VARCHAR | `` |
| `programs` | Programmes ou festivals auxquels l'événement est associé. | VARCHAR | `L'Été du Canal ; Paris Plages` |
| `address_url` | Lien vers un événement en ligne. | VARCHAR | `https://zoom.us/j/123456789` |
| `address_url_text`| Informations complémentaires sur le lien de l'événement en ligne. | VARCHAR | `Conférence en direct sur Zoom` |
| `address_text` | Compléments d'information sur un lieu (ex: bâtiment, étage...). | VARCHAR | `Retransmis depuis l'Auditorium` |
| `title_event` | Titre court ou libellé de l'événement. | VARCHAR | `Été du Canal` |
| `audience` | Public cible de l'événement. | VARCHAR | `Tout public / Jeune public / Enfants ...` |
| `childrens` | Indique si l'événement est adapté aux enfants. | VARCHAR | `Oui, à partir de 6 ans / Non` |
| `group` | Indique si l'événement est adapté aux groupes. | VARCHAR | `Oui, sur réservation / Non` |
| `locale` | Langue principale de l'événement. | VARCHAR | `fr / en` |
| `rank` | Classement ou popularité de l'événement. | NUMBER | `932.5` |
| `weight` | ... | INTEGER | `100` |
| `qfap_tags` | Catégories ou mots-clés associés à l'événement. | VARCHAR | `Concert ;Festival ;Sport` |
| `universe_tags` | Mots-clés d'univers thématique plus larges. | VARCHAR | `Musique ; Loisirs ; Famille` |
| `event_indoor` | Indique si l'événement se déroule en intérieur (1) ou extérieur (0). | INTEGER | `0 / 1` |
| `event_pets_allowed` | Indique si les animaux de compagnie sont autorisés. | INTEGER | `1 / 0` |
| `contact_organisation_name`| Nom de l'organisation de contact. | VARCHAR | `Association des Canaux de Paris` |
| `contact_url_text`| Texte associé à l'URL de contact. | VARCHAR | `Visitez notre site` |
| `contact_vimeo` | URL de la page Vimeo associée. | VARCHAR | `https://vimeo.com/bel_ete_canal` |
| `contact_deezer`| URL de la page Deezer associée. | VARCHAR | `https://deezer.com/playlist/12345` |
| `contact_tiktok` | URL du compte TikTok associé. | VARCHAR | `https://tiktok.com/@bel_ete_canal` |
| `contact_twitch`| URL de la chaîne Twitch associée. | VARCHAR | `https://twitch.tv/bel_ete_canal` |
| `contact_spotify`| URL de la playlist Spotify associée. | VARCHAR | `https://spotify.com/playlist/abcde` |
| `contact_youtube`| URL de la chaîne YouTube associée. | VARCHAR | `https://youtube.com/c/belelecanal` |
| `contact_bandcamp`| URL de la page Bandcamp associée. | VARCHAR | `https://belelecanal.bandcamp.com` |
| `contact_linkedin`| URL de la page LinkedIn associée. | VARCHAR | `https://linkedin.com/company/bel-ete-canal` |
| `contact_snapchat`| URL du compte Snapchat associé. | VARCHAR | `https://snapchat.com/add/bel_ete_canal` |
| `contact_whatsapp`| Lien ou numéro WhatsApp de contact. | VARCHAR | `https://wa.me/33123456789` |
| `contact_instagram`| URL du compte Instagram associé. | VARCHAR | `https://instagram.com/bel_ete_canal` |
| `contact_messenger`| Lien vers un contact Messenger. | VARCHAR | `https://m.me/bel.ete.canal` |
| `contact_pinterest`| URL du compte Pinterest associé. | VARCHAR | `https://pinterest.com/bel_ete_canal` |
| `contact_soundcloud`| URL de la page Soundcloud associée. | VARCHAR | `https://soundcloud.com/bel_ete_canal` |

</details>

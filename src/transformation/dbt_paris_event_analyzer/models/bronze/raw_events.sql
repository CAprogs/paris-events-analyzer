

SELECT *
FROM read_parquet('{{ get_today_file("parquet") }}')

from proton_driver import client
client = client.Client(host='localhost', port=8463)

client.execute(f"""
DROP STREAM token_strict_raw;
""")
client.execute(f"""
DROP STREAM token_all_raw;
""")

client.execute(f"""
CREATE MUTABLE STREAM token_strict_raw
(
  `address` string,
  `chainId` integer,
  `decimals` integer,
  `name` string,
  `symbol` string,
  `logoURI` string,
  `tags` array(string),
  `extensions` map(string, string)        
)
PRIMARY KEY (address) SETTINGS shards=3;
""")

client.execute(f"""
CREATE MUTABLE STREAM token_all_raw
(
  `address` string,
  `chainId` integer,
  `decimals` integer,
  `name` string,
  `symbol` string,
  `logoURI` string,
  `tags` array(string),
  `extensions` map(string, string)        
)
PRIMARY KEY (address) SETTINGS shards=3;
""")

client.execute(f"""
CREATE MATERIALIZED VIEW jupiter_tokens AS
WITH cte1 AS
  (
    SELECT
      true AS is_strict, *
    FROM
      token_strict_raw
  ), cte2 AS
  (
    SELECT
      token_all_raw.*, cte1.is_strict
    FROM
      token_all_raw
    LEFT JOIN cte1 ON token_all_raw.address = cte1.address
  ), cte3 AS
  (
    SELECT
      *, extensions['isBanned'] AS is_banned
    FROM
      cte2
  )
SELECT
  *, multi_if(is_strict, 'strict', is_banned = 'true', 'banned', 'all') AS jup_token_type
FROM cte3
""")
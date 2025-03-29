LOAD CSV FROM '/var/lib/memgraph/minic_data.csv' WITH HEADER AS row

MERGE (sender:Account {account_id: row.account})
ON CREATE SET sender.bank = row.from_bank

MERGE (receiver:Account {account_id: row["account.1"]})
ON CREATE SET receiver.bank = row.to_bank

MERGE (tr:Transaction {transaction_id: toString(row.timestamp) + "-" + toString(rand())})
ON CREATE SET
  tr.timestamp = localdatetime(row.timestamp),
  tr.amount_received = tofloat(row.amount_received),
  tr.receiving_currency = row.receiving_currency,
  tr.amount_paid = tofloat(row.amount_paid),
  tr.payment_currency = row.payment_currency,
  tr.payment_format = row.payment_format,
  tr.is_laundering = toInteger(row.is_laundering)

MERGE (sender) -[:FROM]->(tr)
MERGE (tr) -[:TO]->(receiver)

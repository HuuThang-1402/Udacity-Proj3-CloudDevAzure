import psycopg2

# Update connection string information

host = "udaproj3-sv.postgres.database.azure.com"
dbname = "techconfdb"
user = "azureadmin@udaproj3-sv"
password = "Udathangnh36"
sslmode = "require"

# Construct connection string

conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)
conn = psycopg2.connect(conn_string)
print("Connection established")
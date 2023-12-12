from server.db.firebase_connections import firabase_connection

x = firabase_connection()
x.add("test@test.com", "pkeytest", "1.1.2020", "1.2.2020")
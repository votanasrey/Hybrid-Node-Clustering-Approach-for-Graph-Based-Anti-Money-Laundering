from utils.telegram_service import send_telegram_message
import datetime

message = f'''
<pre>
=======================================
FLATFILE TO POSGRESQL DATA PIPELINE
=======================================

SOURCE: FLATFILE - large_trans.csv
DESTINATION: POSTGRESQL - localhost
DATABASE: general_db
STATUS: SUCCESS
LOAD DATETIME: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
</pre>
'''

send_telegram_message(message)
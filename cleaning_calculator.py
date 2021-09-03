import re
import sqlite3
import pandas as pd
from datetime import datetime

def calculate_total(cleaning_list):
    apt_lst = re.findall(r'\w+', cleaning_list)
    total_cost = 0
    for apt in apt_lst:
        if 'FP308' in apt:
            total_cost += 60
        elif 'NL461' in apt:
            total_cost += 50
        elif 'MS307' in apt:
            total_cost += 45
        elif 'HS407' in apt:
            total_cost += 45
        else:
            total_cost += 0
    return 'Total: ' + str(total_cost)

def get_query_results():
    conn = sqlite3.connect('/Users/tracygoss/Library/Messages/chat.db')
    cur1 = conn.cursor()
    cur1.execute('''SELECT datetime(m.date / 1000000000 + strftime ("%s", "2001-01-01"), "unixepoch", "localtime") AS message_date,
                 text
             FROM chat c
                JOIN chat_message_join cmj ON c."ROWID" = cmj.chat_id
                JOIN message m ON cmj.message_id = m."ROWID"
             WHERE c.chat_identifier = "+12064290405" and m.is_sent = 1
             ORDER BY m.date DESC
             LIMIT 10; ''')
    
    results = ''
    for message_data in cur1.fetchall():
        print(message_data)
        results += str(message_data)
    return results
    

text_messages = get_query_results()

print(text_messages + '\n' + calculate_total(text_messages))

# cleaning_lst = '''
# 8/23: MS307 FP308 HS407
# 8/24: NL461 FP308
# 8/25: HS407
# 8/26: MS307 HS407
# 8/27: MS307 NL461
# 8/28: FP308
# 8/29: FP308
# '''


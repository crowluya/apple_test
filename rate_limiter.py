import mysql.connector
import redis
import time
import requests
from flask import Flask, request

mydb = mysql.connector.connect(
  host="mysql",
  user="root",
  password="password",
  database="rate_limiter"
)

r = redis.Redis(host='redis', port=6379, db=0)

mycursor = mydb.cursor()

# max tps 1 sec
tps = 100

# limit user req times
def rate_limit(ip_address, user_id):
    # now time
    timestamp = time.time()

    # check 1 sec user req times
    count = r.get(f"{ip_address}_{user_id}")
    if count is None:
        count = 0
    else:
        count = int(count)
    if count >= tps:
        return False

    sql = "INSERT INTO request_logs (ip_address, user_id) VALUES (%s, %s)"
    val = (ip_address, user_id)
    mycursor.execute(sql, val)
    mydb.commit()

    # update redis cache
    r.set(f"{ip_address}_{user_id}", count+1, ex=1)

    return True

def validate_user(user_id, api_key):
    # db check user info
    sql = "SELECT * FROM users WHERE user_id = %s AND api_key = %s"
    val = (user_id, api_key)
    mycursor.execute(sql, val)
    result = mycursor.fetchone()
    if result is None:
        return False
    else:
        return True

app = Flask(__name__)

@app.route('/')
def index():
    user_id = request.args.get('user_id')
    api_key = request.args.get('api_key')
    if user_id is None or api_key is None:
        return 'Missing user_id or api_key', 400

    # user check
    if not validate_user(user_id, api_key):
        return 'Invalid user_id or api_key', 401

    if rate_limit(request.remote_addr, user_id):
        # 允许请求通过
        response = requests.get('https://api.foo.com/api')
        return response.content, response.status_code
    else:
        # 请求被限制
        return 'Too many requests, please wait ', 429

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
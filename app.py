from flask import Flask, render_template, request, jsonify
import redis
from redisUtil import RedisHandler
# make flask server that displays all the colors in redis database
# make flask server that displays all the colors in redis database


def go():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config['REDIS_URL'] = "redis://localhost:6379/0"
    return app


app = go()
redis_client = redis.StrictRedis.from_url(app.config['REDIS_URL'])


@app.route('/')
def index():
    try:
        colors = [color.decode('utf-8')
                  for color in redis_client.hkeys('colors')]
        print("Colors retrieved from Redis:", colors)
        return render_template('index.html', colors=colors)
    except Exception as e:
        print("Error fetching colors from Redis:", str(e))
        return "Error fetching colors from Redis."


if __name__ == '__main__':
    app.run(port=8080, debug=True)

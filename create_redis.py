import redis
import os


def go():
    r = redis.Redis(host='localhost', port=6379, db=0)

    r.flushdb()

    with open("data.csv", "r") as colors:
        for line in colors:
            line = line.strip()
            name, number = line.split(",")
            number = int(number)
            r.hset("colors", name, number)


if __name__ == '__main__':
    print("Creating redis database")
    go()

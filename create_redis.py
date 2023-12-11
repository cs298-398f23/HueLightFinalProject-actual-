import redis
import os


def go():
    r = redis.Redis(host='localhost', port=6379, db=0)

    r.flushdb()

    with open("data.csv", "r") as colors:
        for line in colors:
            line = line.strip()
            name, rgb, count = line.split(",")
            rbg = int(rgb)
            count = int(count)
            r.hset("colors", name, rgb, count)
            print(f"Added {name} with {rgb} and {count} to redis database.")


if __name__ == '__main__':
    print("Creating redis database")
    go()

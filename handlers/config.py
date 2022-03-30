"""CONFIG FILE"""
from handlers.imports import *
'''REDIS'''

REDIS_HOST = 'redis-13333.c55.eu-central-1-1.ec2.cloud.redislabs.com'
REDIS_PORT = 13333
REDIS_PASS = '97U47jS9DPzKzNxI5OLxZYCVXc1e6CiR'

r = redis.StrictRedis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    charset="utf-8",
    decode_responses=True,
    password=REDIS_PASS
)

colors = {
    'background': '#242221',
    'text': '#5867db'
}

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll',
        'background-color': '#242221',
        'color': '#5867db'
    },

    'H4': {
        'border': 'thin lightgrey solid',
        'background-color': '#242221',
        'color': '#ad2300',
        'box-sizing': 'border-box',
        'padding': '10px'
    },
    'H5': {
        'border': 'thin lightgrey solid',
        'background-color': '#242221',
        'color': '#ad2300',
        'box-sizing': 'border-box',
        'padding': '10px'
    },
    'DIV': {
        'border': 'thin lightgrey solid',
        'background-color': '#242221',
        'color': '#5867db',
        'box-sizing': 'border-box',
        'padding': '10px'
    }
}


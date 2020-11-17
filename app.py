import os
import time
import io
from flask import Flask, jsonify, render_template, send_file
from helpers import convert_unixepoch_to_time
from config import Config, cache

app = Flask(__name__)


@app.route('/env')
def env():
    env_list = {}
    for item, value in os.environ.items():
        env_list[item] = value
    return jsonify(env_list)


@app.route('/')
def main():
    mask_count = cache.get('mask_count').decode() if cache.get('mask_count') else 0
    nomask_count = cache.get('nomask_count').decode() if cache.get('nomask_count') else 0
    timestamp = convert_unixepoch_to_time(time.time())
    return render_template('index.html',
                           mask_count=mask_count,
                           nomask_count=nomask_count,
                           timestamp=timestamp,
                           barcodes=[],
                           refreshInterval=Config.REFRESH_INTERVAL,
                           camera_name=Config.LOCATION,
                           version=Config.VERSION)


@app.route('/image_still')
def image_still():
    image = cache.get('image')
    if image:
        return send_file(io.BytesIO(image), mimetype='image/jpeg')
    else:
        return send_file('static/no_feed.jpeg', mimetype='image/jpeg')


@app.route('/api')
def api():
    mask_count = cache.get('mask_count').decode() if cache.get('mask_count') else 0
    nomask_count = cache.get('nomask_count').decode() if cache.get('nomask_count') else 0
    timestamp = convert_unixepoch_to_time(time.time())
    api = {'image_timestamp': timestamp, 'mask_count': mask_count, 'nomask_count': nomask_count}
    return jsonify(api)


if __name__ == '__main__':
    app.run()

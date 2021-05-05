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
                           refreshInterval=Config.REFRESH_INTERVAL,
                           cam1_name=Config.CAM1_NAME,
                           cam2_name=Config.CAM2_NAME,
                           cam3_name=Config.CAM3_NAME,
                           cam4_name=Config.CAM4_NAME,
                           version=Config.VERSION)


@app.route('/image/<name>')
def image_feed(name):
    image = cache.get(f'{name}-image')
    if image:
        return send_file(io.BytesIO(image), mimetype='image/jpeg')
    else:
        return send_file('static/no_feed.jpeg', mimetype='image/jpeg')


@app.route('/api')
def api():
    mask_count_cam1 = cache.get(f'{Config.CAM1}-mask_count').decode() if cache.get(f'{Config.CAM1}-mask_count') else 0
    nomask_count_cam1 = cache.get(f'{Config.CAM1}-nomask_count').decode() if cache.get(f'{Config.CAM1}-nomask_count') else 0

    mask_count_cam2 = cache.get(f'{Config.CAM2}-mask_count').decode() if cache.get(f'{Config.CAM2}-mask_count') else 0
    nomask_count_cam2 = cache.get(f'{Config.CAM2}-nomask_count').decode() if cache.get(f'{Config.CAM2}-nomask_count') else 0

    mask_count_cam3 = cache.get(f'{Config.CAM3}-mask_count').decode() if cache.get(f'{Config.CAM3}-mask_count') else 0
    nomask_count_cam3 = cache.get(f'{Config.CAM3}-nomask_count').decode() if cache.get(f'{Config.CAM3}-nomask_count') else 0

    mask_count_cam4 = cache.get(f'{Config.CAM4}-mask_count').decode() if cache.get(f'{Config.CAM4}-mask_count') else 0
    nomask_count_cam4 = cache.get(f'{Config.CAM4}-nomask_count').decode() if cache.get(f'{Config.CAM4}-nomask_count') else 0

    timestamp = convert_unixepoch_to_time(time.time())
    api = {'image_timestamp': timestamp,
           'mask_count_cam1': mask_count_cam1, 'nomask_count_cam1': nomask_count_cam1,
           'mask_count_cam2': mask_count_cam2, 'nomask_count_cam2': nomask_count_cam2,
           'mask_count_cam3': mask_count_cam3, 'nomask_count_cam3': nomask_count_cam3,
           'mask_count_cam4': mask_count_cam4, 'nomask_count_cam4': nomask_count_cam4,
           }
    return jsonify(api)


if __name__ == '__main__':
    app.run()

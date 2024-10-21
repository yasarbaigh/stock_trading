from angel_one.configs import BASE_PREFIX
from common_utils.log_utils import LogUtils

LogUtils(BASE_PREFIX + "/opt/tmp/angel_1/angel_api_{}.log")

logger_obj = LogUtils.return_logger(__name__)
logger_obj.info('Starting algo now !!')

import threading
import time

from FLASK_CONFIGS import SELECTED_STOCK, SELECTED_STRIKE, SELECTED_LOT, SELECTED_TF, ACTION_START, ACTION, THREAD_KEY, \
    THREAD_OBJT, ACTION_STOP, STRATEGY, STRATEGY_HEIKIN_ASHI, SELECTED_DATE, SELECTED_OPTIONS, PUNCHED_AT, REASON
from datetime import datetime
# ZZZ make sure u dont change above snippet
from angel_one.angel_connector import AngelConnector
from strategies.srini_strategies import hekin_aashi_in_index_strikes
from flask_cors import CORS

conn = AngelConnector()
conn.generate_smart_api_session()

from flask import Flask, request, jsonify
from threading import Thread

app = Flask('Angel_Flask')
# CORS(app, resources={r"/*": {"origins": ["http://localhost:3002", "http://127.0.0.1:3002"
#                                                                   "http://chyr.duckdns.org:3002",
#                                          'http://192.168.0.109:3002', 'http://my_pv_ip:3002'],
#                              "supports_credentials": True}})

# allow allow origins
CORS(app, resources={r"/*": {"origins": '*', "supports_credentials": True}})

MAIN_THERADS = {}
STOPPED_THERADS = {}


@app.route('/api/get_running', methods=["GET", 'POST'])
def add_guide():
    logger_obj.info(MAIN_THERADS)

    op = []
    stopped_op = []
    for k, v in MAIN_THERADS.items():
        ele = {'name': k}
        for k1, v1 in v.items():
            if k1 == THREAD_OBJT:
                continue
            ele[k1] = v1
        op.append(ele)

    for k, v in STOPPED_THERADS.items():
        ele = {'name': k}
        for k1, v1 in v.items():
            if k1 == THREAD_OBJT:
                continue
            ele[k1] = v1
        stopped_op.append(ele)

    return jsonify({'message': op, 'stopped': stopped_op}), 200


@app.route('/api/start_pattern', methods=['GET', "POST"])
def start_pattern():
    start_args = {}
    if request.is_json:
        json_data = request.get_json()
        start_args[SELECTED_STOCK] = json_data.get(SELECTED_STOCK)
        start_args[SELECTED_TF] = json_data.get(SELECTED_TF)
        start_args[SELECTED_STRIKE] = json_data.get(SELECTED_STRIKE)
        start_args[SELECTED_LOT] = json_data.get(SELECTED_LOT)
        start_args[ACTION] = ACTION_START
        start_args[STRATEGY] = json_data.get(STRATEGY)
        start_args[SELECTED_DATE] = json_data.get(SELECTED_DATE)
        start_args[SELECTED_OPTIONS] = json_data.get(SELECTED_OPTIONS)
        start_args[PUNCHED_AT] = datetime.now().strftime('_%H_%M_%S')

        thread_key = start_args[STRATEGY] + '_' + start_args.get(SELECTED_STOCK) + '_' + start_args[
            SELECTED_DATE] + '_' + start_args.get(SELECTED_TF) + \
                     '_' + start_args.get(SELECTED_STRIKE) + '_' + start_args[SELECTED_OPTIONS] + '_' + start_args.get(
            SELECTED_LOT)

        start_args[THREAD_KEY] = thread_key

        logger_obj.info('Received a START combo {}'.format(thread_key))
        if MAIN_THERADS.get(thread_key):
            logger_obj.info('Received a START combo  {} , but already running'.format(thread_key))
            return jsonify({"message": "Combo {} already running.".format(thread_key)}), 204
        else:
            MAIN_THERADS[thread_key] = start_args
            # Start a new thread to process the data
            thread = Thread(target=trigger_pattern_in_thread, name=thread_key, args=(conn, start_args))
            start_args[THREAD_OBJT] = thread
            thread.start()
            logger_obj.info("Combo Heikin-Ashi started")
            return jsonify({"message": "Combo Heikin-Aashi started"}), 201
    else:
        return jsonify({"message": "Failed ."}), 400


@app.route('/api/stop_pattern', methods=['GET', "POST"])
def stop_pattern():
    thread_key = ''
    try:
        stop_args = {}
        if request.is_json:
            json_data = request.get_json()
            stop_args[SELECTED_STOCK] = json_data.get(SELECTED_STOCK)
            stop_args[SELECTED_TF] = json_data.get(SELECTED_TF)
            stop_args[SELECTED_STRIKE] = json_data.get(SELECTED_STRIKE)
            stop_args[ACTION] = ACTION_STOP
            stop_args[SELECTED_LOT] = json_data.get(SELECTED_LOT)
            stop_args[STRATEGY] = json_data.get(STRATEGY)
            stop_args[SELECTED_DATE] = json_data.get(SELECTED_DATE)
            stop_args[SELECTED_OPTIONS] = json_data.get(SELECTED_OPTIONS)

            thread_key = stop_args[STRATEGY] + '_' + stop_args.get(SELECTED_STOCK) + '_' + stop_args[
                SELECTED_DATE] + '_' + stop_args.get(SELECTED_TF) + \
                         '_' + stop_args.get(SELECTED_STRIKE) + '_' + stop_args[SELECTED_OPTIONS] + '_' + stop_args.get(
                SELECTED_LOT)

            logger_obj.info('Received a STOP combo {}'.format(thread_key))
            if MAIN_THERADS.get(thread_key):
                vl = MAIN_THERADS.get(thread_key)
                vl[ACTION] = ACTION_STOP
                return jsonify({"message": "Combo {} stopping.".format(thread_key)}), 200
            else:
                return jsonify({"message": "Combo Not Available. "}), 200
        else:
            return jsonify({"message": "Failed ."}), 400
    except Exception as e:
        logger_obj.error('stop request error {}'.format(e))
        return jsonify({"message": "Failed {}.".format(e)}), 400
    finally:
        MAIN_THERADS.pop(thread_key, None)


@app.route('/api/simple_stop', methods=['GET', "POST"])
def simple_stop_pattern():
    thread_key = ''
    try:
        stop_args = {}
        if request.is_json:
            json_data = request.get_json()
            thread_key = json_data.get(THREAD_KEY)

            logger_obj.info('Received a STOP combo {}'.format(thread_key))
            if MAIN_THERADS.get(thread_key):
                vl = MAIN_THERADS.get(thread_key)
                vl[ACTION] = ACTION_STOP
                vl[REASON] = 'Manually Stopped.'
                return jsonify({"message": "Combo {} stopping.".format(thread_key)}), 200
            else:
                return jsonify({"message": "Combo Not Available. "}), 200
        else:
            return jsonify({"message": "Failed ."}), 400
    except Exception as e:
        logger_obj.error('stop request error {}'.format(e))
        return jsonify({"message": "Failed {}.".format(e)}), 400
    finally:
        pass


def trigger_pattern_in_thread(conn, thread_args):
    try:
        print('STARTing THREAD: {}'.format(thread_args))
        current_thread = threading.current_thread()
        logger_obj.info(f"Thread '{current_thread.name}' started")

        if thread_args.get(STRATEGY) == STRATEGY_HEIKIN_ASHI:
            hekin_aashi_in_index_strikes(conn, thread_args)

        logger_obj.info(f"Thread '{current_thread.name}' stopping...")
        time.sleep(10)
        logger_obj.info(f"Thread '{current_thread.name}' completely stopped...")
    except Exception as e:
        logger_obj.error('Error in trigger_pattern_in_thread {}'.format(e))
    finally:
        STOPPED_THERADS[thread_args.get(THREAD_KEY)] = thread_args
        MAIN_THERADS.pop(thread_args.get(THREAD_KEY), None)


def trigger_heikin_aashi_RAW(conn, thread_args):
    print('STARTing THREAD: {}'.format(thread_args))
    current_thread = threading.current_thread()
    logger_obj.info(f"Thread '{current_thread.name}' started")

    while thread_args.get(ACTION) == ACTION_START:
        # Perform some work here
        logger_obj.info(f"Thread '{current_thread.name}' is running...")
        time.sleep(1)  # Simulate some work

    logger_obj.info(f"Thread '{current_thread.name}' stopping...")
    time.sleep(10)
    logger_obj.info(f"Thread '{current_thread.name}' completely stopped...")


# Run the Flask app
if __name__ == '__main__':
    app.run(port=3003, host='0.0.0.0')
    app.run(debug=True)
    app.name = 'Angel_Flask'

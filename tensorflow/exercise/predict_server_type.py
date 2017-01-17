#!/usr/bin/env python
# -*- coding: utf-8 -*-
# FileName  : predict_server_type.py
# Author    : wuqingfeng@

import os
import time
import numpy as np
import tensorflow as tf
from datetime import datetime
from collections import OrderedDict
import elasticsearch.helpers
from elasticsearch import Elasticsearch
from netaddr import IPAddress, IPNetwork
from sklearn.preprocessing import normalize

esconfig = {
    "hosts": [{"host": "10.5.0.183", "port": 9200}],
    "maxsize": 25
}

class_num = 16
server_type_num = 5
field_list = ["fp", "lp", "sl", "a1", "a2", "p1", "p2", "pr"]
server_type_dict = {
    "dns_server": 0,
    "person_compute": 1,
    "web_server": 2,
    "outter_server": 3,
    "inner_server": 4
}
save_path = "/opt/workplace/tensorsave/model.ckpt"

es = Elasticsearch(**esconfig)

def int2ip(ipint):
    try:
        t = []
        for i in range(3,-1,-1):
            t.append(str(ipint/(256**i)%256))
        return '.'.join(t)
    except Exception,e:
        return ''

def ip2int(data):
    try:
        intip = 0
        for j,i in enumerate(data.split('.')[::-1]):
            intip = intip + 256**j*int(i)
        return intip
    except Exception,e:
        return 0

def get_session_name(date_int):
    date_str = datetime.fromtimestamp(date_int).strftime("%Y-%m-%d")
    date_list = date_str.split("-")
    date_list[0] = date_list[0][-2:]
    session_name = "sessions-" + "".join(date_list)
    return session_name

def export_feature_ip(ip, starttime=None):
    query = {
        "query": {
            "bool": {
                "must": [
                    { "range": {"lp": {} } },
                    { "term": { "a2": 0 } }
                ]
            }
        },
        "sort": [
            {"fp": {
                    "order": "desc"
                }
            }
        ],
        "_source": field_list
    }

    now = datetime.now()
    ipint = ip2int(ip)
    query["query"]["bool"]["must"][1]["term"]["a2"] = ipint

    if isinstance(starttime, basestring):
        starttime = datetime.strptime(starttime, "%Y-%m-%dT%H:%M:%S")

    if starttime is None:
        endtime = int(time.mktime(now.timetuple()))
        starttime = endtime - 5 * 60
    else:
        starttime = int(time.mktime(starttime.timetuple()))
        endtime = starttime + 5 * 60
    # print starttime, endtime
    records = []
    feature_list = []
    while not records:
        query["query"]["bool"]["must"][0]["range"]["lp"] = {"from": starttime, "to": endtime}
        session_name = get_session_name(endtime)
        iterator = elasticsearch.helpers.scan(es, query=query, scroll='2m', size=10000, index=session_name, doc_type='session', timeout="60s")
        records = list(iterator)
        if records:
            feature_dict = OrderedDict([("is_src_outter", 0), ("is_22_open", 0), ("is_23_open", 0), ("is_25_open", 0), ("is_53_open", 0),
                                ("is_web_open", 0), ("is_137_open", 0), ("is_161_open", 0), ("is_3389_open", 0), ("is_high_open", 0),
                                ("is_http_request", 0), ("is_same_netaddr", 0), ("is_other_netaddr", 0), ("request_count", 0), ("port_count", 0), ("src_ip_count", 0)])
            dst_port_list = []
            src_ip_list = []
            count = 0
            for record in records:
                count += 1
                data = record.get("_source", {})
                if data:
                    src_ip = int2ip(data["a1"])
                    dst_ip = int2ip(data["a2"])
                    src_port = data["p1"]
                    dst_port = data["p2"]
                    pr = data["pr"]
                    # print src_ip, src_port, dst_ip, dst_port, pr
                    # print dst_ip, dst_port
                    if not IPAddress(src_ip).is_private():
                        feature_dict["is_src_outter"] = 1
                    if IPNetwork(src_ip+"/16") == IPNetwork(dst_ip+"/16"):
                        feature_dict["is_same_netaddr"] = 1
                    else:
                        feature_dict["is_other_netaddr"] = 1
                    if src_ip not in src_ip_list:
                        src_ip_list.append(src_ip)
                    if dst_port not in dst_port_list:
                        dst_port_list.append(dst_port)
                    if dst_port in [80, 8080, 443, 8443, 8000]:
                        feature_dict["is_web_open"] = 1
                        if pr == 6:
                            feature_dict["is_http_request"] = 1
                    if dst_port > 1024:
                        feature_dict["is_high_open"] = 1
                        if dst_port == 3389:
                            feature_dict["is_3389_open"] = 1
                    else:
                        if dst_port == 22:
                            feature_dict["is_22_open"] = 1
                        elif dst_port == 23:
                            feature_dict["is_23_open"] = 1
                        elif dst_port == 25:
                            feature_dict["is_25_open"] = 1
                        elif dst_port == 53:
                            feature_dict["is_53_open"] = 1
                        elif dst_port == 137:
                            feature_dict["is_137_open"] = 1
                        elif dst_port == 161:
                            feature_dict["is_161_open"] = 1

            feature_dict["request_count"] = count
            feature_dict["port_count"] = len(dst_port_list)
            feature_dict["src_ip_count"] = len(src_ip_list)

            feature_list = feature_dict.values()
            break
        else:
            if starttime is None:
                endtime = starttime
                starttime = endtime - 5 * 60
            else:
                starttime = endtime
                endtime = starttime + 5 * 60

    return feature_list

def predict_server_type(feature_list):
    # feature_dataset = normalize([feature_list]
    feature_dataset = np.array([feature_list], np.float32)
    feature_dataset = normalize(feature_dataset, axis=1)

    # print feature_dataset

    layer_cnt = 3
    hidden_node_count = 8
    hidden_stddev = np.sqrt(2.0 / 16)
    keep_prob = 0.5
    beta_value = 0.00001

    graph = tf.Graph()
    with graph.as_default():
        tf_dataset = tf.constant(feature_dataset)

        weights1 = tf.Variable(tf.truncated_normal([class_num, hidden_node_count], stddev=hidden_stddev))
        biases1 = tf.Variable(tf.zeros([hidden_node_count]))

        weights = []
        biases = []
        hidden_cur_cnt = hidden_node_count
        for i in range(layer_cnt - 2):
            if hidden_cur_cnt > 2:
                hidden_next_cnt = int(hidden_cur_cnt / 2)
            else:
                hidden_next_cnt = 2
            hidden_stddev = np.sqrt(2.0 / hidden_cur_cnt)
            weights.append(tf.Variable(tf.truncated_normal([hidden_cur_cnt, hidden_next_cnt], stddev=hidden_stddev)))
            biases.append(tf.Variable(tf.zeros([hidden_next_cnt])))
            hidden_cur_cnt = hidden_next_cnt

        test_y0 = tf.matmul(tf_dataset, weights1) + biases1
        test_hidden = tf.nn.relu(test_y0)

        #middle layer
        for i in range(layer_cnt - 2):
            test_y0 = tf.matmul(test_hidden, weights[i]) + biases[i]
            test_hidden = tf.nn.relu(test_y0)

        # last weight
        weights2 = tf.Variable(tf.truncated_normal([hidden_cur_cnt, server_type_num], stddev=hidden_stddev / 2))
        biases2 = tf.Variable(tf.zeros([server_type_num]))

        test_predict = tf.matmul(test_hidden, weights2) + biases2

        test_prediction = tf.nn.softmax(test_predict)

    with tf.Session(graph=graph) as session:
        saver = tf.train.Saver()
        saver.restore(session, save_path)
        testprediction = test_prediction.eval()

    server_type_code = np.argmax(testprediction, 1)[0]
    server_type = server_type_map.get(server_type_code)
    return server_type


if __name__ == "__main__":
    server_type_map = dict(zip(server_type_dict.values(), server_type_dict.keys()))
    test_data = {
        "ip": "10.5.1.19",
        "starttime": "2017-01-17T15:17:03"
    }

    feature_list = export_feature_ip(**test_data)
    server_type = predict_server_type(feature_list)
    print server_type
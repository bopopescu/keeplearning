#!/usr/bin/env python
# -*- coding: utf-8 -*-
# FileName  : model_restore_test.py
# Author    : wuqingfeng@

import numpy as np
import tensorflow as tf
import cPickle as pickle

## need to use the tensorflow >= 0.12.0

class_num = 16
server_type_num = 5
feature_dataset_dir = "/opt/downloads/feature_dataset/"
save_path = "/opt/workplace/tensorsave/model.ckpt"

def accuracy(predictions, labels):
    return (100.0 * np.sum(np.argmax(predictions, 1) == np.argmax(labels, 1)) / predictions.shape[0])


def test():
    pickle_file = feature_dataset_dir + "server_dataset.pickle"

    dataset_struct = [
        ("test_num_list", "test_dataset_list", "test_feature_dataset", "test_label_dataset"),
        ("valid_num_list", "valid_dataset_list", "valid_feature_dataset", "valid_label_dataset"),
        ("train_num_list", "train_dataset_list", "train_feature_dataset", "train_label_dataset"),
    ]

    with open(pickle_file, 'rb') as f:
        merge_dict = pickle.load(f)
        test_feature_dataset = merge_dict["test_feature_dataset"]
        test_label_dataset = merge_dict["test_label_dataset"]
        # valid_feature_dataset = merge_dict["valid_feature_dataset"]
        # valid_label_dataset = merge_dict["valid_label_dataset"]
        # train_feature_dataset = merge_dict["train_feature_dataset"]
        # train_label_dataset = merge_dict["train_label_dataset"]
        del merge_dict
        print test_feature_dataset.shape, test_label_dataset.shape
        # print valid_feature_dataset.shape, valid_label_dataset.shape
        # print train_feature_dataset.shape, train_label_dataset.shape

    layer_cnt = 3
    hidden_node_count = 8
    hidden_stddev = np.sqrt(2.0 / 16)
    keep_prob = 0.5
    beta_value = 0.00001

    graph = tf.Graph()
    with graph.as_default():
        tf_test_dataset = tf.constant(test_feature_dataset)

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

        test_y0 = tf.matmul(tf_test_dataset, weights1) + biases1
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
        # print testprediction.shape
        print 'Test accuracy: %.1f%%' % accuracy(testprediction, test_label_dataset)

if __name__ == "__main__":
    test()


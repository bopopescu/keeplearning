#!/usr/bin/env python
# -*- coding: utf-8 -*-
# FileName  : full_connect_sgd.py
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

if __name__ == "__main__":
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
        valid_feature_dataset = merge_dict["valid_feature_dataset"]
        valid_label_dataset = merge_dict["valid_label_dataset"]
        train_feature_dataset = merge_dict["train_feature_dataset"]
        train_label_dataset = merge_dict["train_label_dataset"]
        del merge_dict
        print test_feature_dataset.shape, test_label_dataset.shape
        print valid_feature_dataset.shape, valid_label_dataset.shape
        print train_feature_dataset.shape, train_label_dataset.shape

    dropout = False
    lrd = True
    regular = True
    layer_cnt = 3
    batch_size = 64
    hidden_node_count = 8
    hidden_stddev = np.sqrt(2.0 / 16)
    keep_prob = 0.5
    beta_value = 0.00001

    graph = tf.Graph()
    with graph.as_default():
        tf_train_dataset = tf.placeholder(tf.float32, shape=(batch_size, class_num))
        tf_train_labels = tf.placeholder(tf.float32, shape=(batch_size, server_type_num))
        tf_valid_dataset = tf.constant(valid_feature_dataset)
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

        y0 = tf.matmul(tf_train_dataset, weights1) + biases1
        hidden = tf.nn.relu(y0)
        hidden_drop = hidden

        if dropout:
            hidden_drop = tf.nn.dropout(hidden, keep_prob)

        #first wx + b for valid
        valid_y0 = tf.matmul(tf_valid_dataset, weights1) + biases1
        valid_hidden = tf.nn.relu(valid_y0)
        #first wx + b for test
        test_y0 = tf.matmul(tf_test_dataset, weights1) + biases1
        test_hidden = tf.nn.relu(test_y0)

        #middle layer
        for i in range(layer_cnt - 2):
            y1 = tf.matmul(hidden_drop, weights[i]) + biases[i]
            hidden_drop = tf.nn.relu(y1)
            if dropout:
                keep_prob += 0.5 * i /(layer_cnt + 1)
                hidden_drop = tf.nn.dropout(hidden_drop, keep_prob)
            
            y0 = tf.matmul(hidden, weights[i]) + biases[i] 
            hidden = tf.nn.relu(y0)
            
            valid_y0 = tf.matmul(valid_hidden, weights[i]) + biases[i]
            valid_hidden = tf.nn.relu(valid_y0)
            
            test_y0 = tf.matmul(test_hidden, weights[i]) + biases[i]
            test_hidden = tf.nn.relu(test_y0)

        # last weight
        weights2 = tf.Variable(tf.truncated_normal([hidden_cur_cnt, server_type_num], stddev=hidden_stddev / 2))
        biases2 = tf.Variable(tf.zeros([server_type_num]))
        #last wx + b
        logits = tf.matmul(hidden_drop, weights2) + biases2
        
        #predicts
        logits_predict = tf.matmul(hidden, weights2) + biases2
        valid_predict = tf.matmul(valid_hidden, weights2) + biases2
        test_predict = tf.matmul(test_hidden, weights2) + biases2
        
        if regular:
            l2_loss = tf.nn.l2_loss(weights1) + tf.nn.l2_loss(biases1) + tf.nn.l2_loss(weights2) + tf.nn.l2_loss(biases2)
            for i in range(len(weights)):
                l2_loss += tf.nn.l2_loss(weights[i])
                l2_loss += tf.nn.l2_loss(biases[i])
            l2_loss *= beta_value
        else:
            l2_loss = 0
        
        loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits, tf_train_labels)) + l2_loss
        
        
        if lrd:
            cur_step = tf.Variable(0, trainable=False)
            starter_learning_rate = 0.2
            learning_rate = tf.train.exponential_decay(starter_learning_rate, cur_step, 10000, 0.96, staircase=True)
            optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss, global_step=cur_step)
        else:
            optimizer = tf.train.GradientDescentOptimizer(0.2).minimize(loss)
            
        #     logits_predict = tf.matmul(hidden, weights2) + biases2
        train_prediction = tf.nn.softmax(logits_predict)
        valid_prediction = tf.nn.softmax(valid_predict)
        test_prediction = tf.nn.softmax(test_predict)

    num_steps = 10001

    with tf.Session(graph=graph) as session:
        tf.global_variables_initializer().run()
        saver = tf.train.Saver()
        print("Initialized")
        for step in range(num_steps):
            offset_range = train_label_dataset.shape[0] - batch_size
            offset = (step * batch_size) % offset_range

            batch_data = train_feature_dataset[offset:(offset + batch_size), :]
            batch_labels = train_label_dataset[offset:(offset + batch_size), :]

            feed_dict = {tf_train_dataset: batch_data, tf_train_labels: batch_labels}

            _, l, predictions = session.run([optimizer, loss, train_prediction], feed_dict=feed_dict)
            
            # print batch_accuracy
            if(step % 500 == 0):
                batch_accuracy = accuracy(predictions, batch_labels)
                validate_accuracy = accuracy(valid_prediction.eval(), valid_label_dataset)
                print "Minibatch loss at step %d: %f" % (step, l)
                print "Minibatch accuracy: %.1f%%" % batch_accuracy
                print 'Validation accuracy: %.1f%%' % validate_accuracy
            # if l < 0.4:
            #     print "Minibatch loss at step %d: %f" % (step, l)
            #     print "Minibatch accuracy: %.1f%%" % batch_accuracy
            #     print 'Validation accuracy: %.1f%%' % validate_accuracy
            #     break
        testprediction = test_prediction.eval()
        # print testprediction.shape
        print 'Test accuracy: %.1f%%' % accuracy(testprediction, test_label_dataset)
        saver.save(session, save_path)
        print "Model stored..."
        print saver.last_checkpoints







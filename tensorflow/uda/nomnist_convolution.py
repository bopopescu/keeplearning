#!/usr/bin/env python
# -*- coding: utf-8 -*-
# FileName  : nomnist_convolution.py
# Author    : wuqingfeng@

from __future__ import print_function
import numpy as np
import tensorflow as tf
from six.moves import cPickle as pickle

## need to use the tensorflow >= 0.12.0

pickle_file = '/opt/download/notMNIST.pickle'
image_size = 28
num_labels = 10
num_channels = 1

def reformat(dataset, labels):
    dataset = dataset.reshape((-1, image_size, image_size, num_channels)).astype(np.float32)
    labels = (np.arange(num_labels) == labels[:,None]).astype(np.float32)
    return dataset, labels

def accuracy(predictions, labels):
    return (100.0 * np.sum(np.argmax(predictions, 1) == np.argmax(labels, 1)) / predictions.shape[0])

def maxpool2d(data, k=2, s=2):
    return tf.nn.max_pool(data, ksize=[1, k, k, 1], strides=[1, s, s, 1], padding='SAME')

def train_with_conv():
    batch_size = 16
    patch_size = 5
    depth = 16
    num_hidden = 64

    graph = tf.Graph()
    with graph.as_default():
        tf_train_dataset = tf.placeholder(tf.float32, shape=(batch_size, image_size, image_size, num_channels))
        tf_train_labels = tf.placeholder(tf.float32, shape=(batch_size, num_labels))
        tf_valid_dataset = tf.constant(valid_dataset)
        tf_test_dataset = tf.constant(test_dataset)
        
        layer1_weights = tf.Variable(tf.truncated_normal([patch_size, patch_size, num_channels, depth], stddev=0.1))
        layer1_biases = tf.Variable(tf.zeros([depth]))
        layer2_weights = tf.Variable(tf.truncated_normal([patch_size, patch_size, depth, depth], stddev=0.1))
        layer2_biases = tf.Variable(tf.constant(1.0, shape=[depth]))
        layer3_weights = tf.Variable(tf.truncated_normal([image_size // 4 * image_size // 4 * depth, num_hidden], stddev=0.1))
        layer3_biases = tf.Variable(tf.constant(1.0, shape=[num_hidden]))
        layer4_weights = tf.Variable(tf.truncated_normal([num_hidden, num_labels], stddev=0.1))
        layer4_biases = tf.Variable(tf.constant(1.0, shape=[num_labels]))
        
        def model(data):
            conv = tf.nn.conv2d(data, layer1_weights, [1, 2, 2, 1], padding='SAME')
            hidden = tf.nn.relu(conv + layer1_biases)
            conv = tf.nn.conv2d(hidden, layer2_weights, [1, 2, 2, 1], padding='SAME')
            hidden = tf.nn.relu(conv + layer2_biases)
            shape = hidden.get_shape().as_list()
            reshape = tf.reshape(hidden, [shape[0], shape[1] * shape[2] * shape[3]])
            hidden = tf.nn.relu(tf.matmul(reshape, layer3_weights) + layer3_biases)
            return tf.matmul(hidden, layer4_weights) + layer4_biases
        
        # Training computation.
        logits = model(tf_train_dataset)
        loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits, tf_train_labels))
        # Optimizer.
        optimizer = tf.train.GradientDescentOptimizer(0.05).minimize(loss)
        # Predictions for the training, validation, and test data.
        train_prediction = tf.nn.softmax(logits)
        valid_prediction = tf.nn.softmax(model(tf_valid_dataset))
        test_prediction = tf.nn.softmax(model(tf_test_dataset))
        
        num_steps = 10001

        with tf.Session(graph=graph) as session:
            tf.global_variables_initializer().run()
            print("Initialized")
            for step in range(num_steps):
                
                offset_range = train_labels.shape[0] - batch_size
                offset = (step * batch_size) % offset_range

                batch_data = train_dataset[offset:(offset + batch_size), :, :, :]
                batch_labels = train_labels[offset:(offset + batch_size), :]
                
                feed_dict = {tf_train_dataset: batch_data, tf_train_labels: batch_labels}
                
                _, l, predictions = session.run([optimizer, loss, train_prediction], feed_dict=feed_dict)
                if(step % 500 == 0):
                    print("Minibatch loss at step %d: %f" % (step, l))
                    print("Minibatch accuracy: %.1f%%" % accuracy(predictions, batch_labels))
                    print('Validation accuracy: %.1f%%' % accuracy(valid_prediction.eval(), valid_labels))
            print('Test accuracy: %.1f%%' % accuracy(test_prediction.eval(), test_labels))

def train_with_max_pool_conv():
    batch_size = 16
    patch_size = 5
    depth = 16
    num_hidden = 64

    graph = tf.Graph()
    with graph.as_default():
        tf_train_dataset = tf.placeholder(tf.float32, shape=(batch_size, image_size, image_size, num_channels))
        tf_train_labels = tf.placeholder(tf.float32, shape=(batch_size, num_labels))
        tf_valid_dataset = tf.constant(valid_dataset)
        tf_test_dataset = tf.constant(test_dataset)
        
        layer1_weights = tf.Variable(tf.truncated_normal([patch_size, patch_size, num_channels, depth], stddev=0.1))
        layer1_biases = tf.Variable(tf.zeros([depth]))
        layer2_weights = tf.Variable(tf.truncated_normal([patch_size, patch_size, depth, depth], stddev=0.1))
        layer2_biases = tf.Variable(tf.constant(1.0, shape=[depth]))
        layer3_weights = tf.Variable(tf.truncated_normal([64, num_hidden], stddev=0.1))
        layer3_biases = tf.Variable(tf.constant(1.0, shape=[num_hidden]))
        layer4_weights = tf.Variable(tf.truncated_normal([num_hidden, num_labels], stddev=0.1))
        layer4_biases = tf.Variable(tf.constant(1.0, shape=[num_labels]))
        
        def model(data):
            conv = tf.nn.conv2d(data, layer1_weights, [1, 2, 2, 1], padding='SAME')
            conv = maxpool2d(conv)
            hidden = tf.nn.relu(conv + layer1_biases)
            conv = tf.nn.conv2d(hidden, layer2_weights, [1, 2, 2, 1], padding='SAME')
            conv = maxpool2d(conv)
            hidden = tf.nn.relu(conv + layer2_biases)

            shape = hidden.get_shape().as_list()
            reshape = tf.reshape(hidden, [shape[0], shape[1] * shape[2] * shape[3]])
            hidden = tf.nn.relu(tf.matmul(reshape, layer3_weights) + layer3_biases)
            return tf.matmul(hidden, layer4_weights) + layer4_biases
        
        # Training computation.
        logits = model(tf_train_dataset)
        loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits, tf_train_labels))
        # Optimizer.
        optimizer = tf.train.GradientDescentOptimizer(0.05).minimize(loss)
        # Predictions for the training, validation, and test data.
        train_prediction = tf.nn.softmax(logits)
        valid_prediction = tf.nn.softmax(model(tf_valid_dataset))
        test_prediction = tf.nn.softmax(model(tf_test_dataset))
        
        num_steps = 10001

        with tf.Session(graph=graph) as session:
            tf.global_variables_initializer().run()
            print("Initialized")
            for step in range(num_steps):
                
                offset_range = train_labels.shape[0] - batch_size
                offset = (step * batch_size) % offset_range

                batch_data = train_dataset[offset:(offset + batch_size), :, :, :]
                batch_labels = train_labels[offset:(offset + batch_size), :]
                
                feed_dict = {tf_train_dataset: batch_data, tf_train_labels: batch_labels}
                
                _, l, predictions = session.run([optimizer, loss, train_prediction], feed_dict=feed_dict)
                if(step % 500 == 0):
                    print("Minibatch loss at step %d: %f" % (step, l))
                    print("Minibatch accuracy: %.1f%%" % accuracy(predictions, batch_labels))
                    print('Validation accuracy: %.1f%%' % accuracy(valid_prediction.eval(), valid_labels))
            print('Test accuracy: %.1f%%' % accuracy(test_prediction.eval(), test_labels))

def train_with_better_conv(drop=False, lrd=False):
    batch_size = 16
    patch_size = 5
    depth = 16
    num_hidden = 64

    graph = tf.Graph()
    with graph.as_default():
        tf_train_dataset = tf.placeholder(tf.float32, shape=(batch_size, image_size, image_size, num_channels))
        tf_train_labels = tf.placeholder(tf.float32, shape=(batch_size, num_labels))
        tf_valid_dataset = tf.constant(valid_dataset)
        tf_test_dataset = tf.constant(test_dataset)
        
        layer1_weights = tf.Variable(tf.truncated_normal([patch_size, patch_size, num_channels, depth], stddev=0.1))
        layer1_biases = tf.Variable(tf.zeros([depth]))
        layer2_weights = tf.Variable(tf.truncated_normal([patch_size, patch_size, depth, depth], stddev=0.1))
        layer2_biases = tf.Variable(tf.constant(1.0, shape=[depth]))
        layer3_weights = tf.Variable(tf.truncated_normal([64, num_hidden], stddev=0.1))
        layer3_biases = tf.Variable(tf.constant(1.0, shape=[num_hidden]))
        layer4_weights = tf.Variable(tf.truncated_normal([num_hidden, num_labels], stddev=0.1))
        layer4_biases = tf.Variable(tf.constant(1.0, shape=[num_labels]))
        
        def model(data):
            conv = tf.nn.conv2d(data, layer1_weights, [1, 2, 2, 1], padding='SAME')
            conv = maxpool2d(conv)
            hidden = tf.nn.relu(conv + layer1_biases)
            if drop:
                hidden = tf.nn.dropout(hidden, 0.5)
            conv = tf.nn.conv2d(hidden, layer2_weights, [1, 2, 2, 1], padding='SAME')
            conv = maxpool2d(conv)
            hidden = tf.nn.relu(conv + layer2_biases)
            if drop:
                hidden = tf.nn.dropout(hidden, 0.7)
            shape = hidden.get_shape().as_list()
            reshape = tf.reshape(hidden, [shape[0], shape[1] * shape[2] * shape[3]])
            hidden = tf.nn.relu(tf.matmul(reshape, layer3_weights) + layer3_biases)
            if drop:
                hidden = tf.nn.dropout(hidden, 0.8)
            return tf.matmul(hidden, layer4_weights) + layer4_biases
        
        # Training computation.
        logits = model(tf_train_dataset)
        loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits, tf_train_labels))
        # Optimizer.
        if lrd:
            cur_step = tf.Variable(0)
            starter_learning_rate = 0.1
            learning_rate = tf.train.exponential_decay(starter_learning_rate, cur_step, 10000, 0.96, staircase=True)
            optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss, global_step=cur_step)
        else:
            optimizer = tf.train.GradientDescentOptimizer(0.05).minimize(loss)
        # Predictions for the training, validation, and test data.
        train_prediction = tf.nn.softmax(logits)
        valid_prediction = tf.nn.softmax(model(tf_valid_dataset))
        test_prediction = tf.nn.softmax(model(tf_test_dataset))
        
        num_steps = 50001

        with tf.Session(graph=graph) as session:
            tf.global_variables_initializer().run()
            print("Initialized")
            for step in range(num_steps):
                
                offset_range = train_labels.shape[0] - batch_size
                offset = (step * batch_size) % offset_range

                batch_data = train_dataset[offset:(offset + batch_size), :, :, :]
                batch_labels = train_labels[offset:(offset + batch_size), :]
                
                feed_dict = {tf_train_dataset: batch_data, tf_train_labels: batch_labels}
                
                _, l, predictions = session.run([optimizer, loss, train_prediction], feed_dict=feed_dict)
                if(step % 500 == 0):
                    print("Minibatch loss at step %d: %f" % (step, l))
                    print("Minibatch accuracy: %.1f%%" % accuracy(predictions, batch_labels))
                    print('Validation accuracy: %.1f%%' % accuracy(valid_prediction.eval(), valid_labels))
            print('Test accuracy: %.1f%%' % accuracy(test_prediction.eval(), test_labels))

if __name__ == "__main__":

    with open(pickle_file, 'rb') as f:
        save = pickle.load(f)
        train_dataset = save['train_dataset']
        train_labels = save['train_labels']
        valid_dataset = save['valid_dataset']
        valid_labels = save['valid_labels']
        test_dataset = save['test_dataset']
        test_labels = save['test_labels']
        del save
        print('Training set', train_dataset.shape, train_labels.shape)
        print('Validating set', valid_dataset.shape, valid_labels.shape)
        print('Tset set', test_dataset.shape, test_labels.shape)

    train_dataset, train_labels = reformat(train_dataset, train_labels)
    valid_dataset, valid_labels = reformat(valid_dataset, valid_labels)
    test_dataset, test_labels = reformat(test_dataset, test_labels)
    print('Training set', train_dataset.shape, train_labels.shape)
    print('Validating set', valid_dataset.shape, valid_labels.shape)
    print('Tset set', test_dataset.shape, test_labels.shape)

    train_with_conv()
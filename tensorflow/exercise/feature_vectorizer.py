#!/usr/bin/env python
# -*- coding: utf-8 -*-
# FileName  : feature_vectorizer.py
# Author    : wuqingfeng@

import numpy as np
import copy
import os
import sys
import cPickle as pickle
from sklearn.preprocessing import normalize

class_num = 16
server_type_num = 5
np.random.seed(124)

def randomize(features, labels):
    permutation = np.random.permutation(labels.shape[0])
    shuffled_features = features[permutation, :]
    shuffled_labels = labels[permutation, :]
    return shuffled_features, shuffled_labels 

def load_feature_dataset(data_dir):
    dataset_files = os.listdir(feature_dataset_dir)
    if "server_dataset.pickle" in dataset_files:
        dataset_files.remove("server_dataset.pickle")

    train_dataset_list = []
    valid_dataset_list = []
    test_dataset_list = []
    train_num_list = []
    valid_num_list = []
    test_num_list = []

    for dataset in dataset_files:
        dataset_path = feature_dataset_dir + dataset
        with open(dataset_path, "rb") as f:
            _dataset = pickle.load(f)
            dataset_item = np.array(_dataset, np.int32)
            np.random.shuffle(dataset_item)
            batch_num = dataset_item.shape[0]
            test_num = int(batch_num * 0.1)
            test_num_list.append(test_num)
            test_dataset_list.append(dataset_item[:test_num])
            data_num = batch_num - test_num
            valid_num = int(data_num * 0.1)
            offset_list = []
            for i in range(data_num/valid_num):
                offset_list.append(valid_num*(i+1))
            data_split_list = np.split(dataset_item[test_num:], offset_list)
            # print len(data_split_list)
            valid_count = 0
            train_count = 0
            t_valid_dataset_list = []
            t_train_dataset_list = []
            for i in range(data_num/valid_num):
                data_split_copy = copy.deepcopy(data_split_list)
                valid_dataset = data_split_copy.pop(i)
                t_valid_dataset_list.append(valid_dataset)
                t_train_dataset_list.extend(data_split_copy)
                valid_count += len(valid_dataset)
                train_count += data_num - len(valid_dataset)
            valid_num_list.append(valid_count)
            train_num_list.append(train_count)
            # print train_count
            valid_dataset_list.append(np.vstack(t_valid_dataset_list))
            # print len(t_train_dataset_list)
            train_dataset_list.append(np.vstack(t_train_dataset_list))
            # print np.vstack(t_train_dataset_list).shape
            del _dataset
    return {
        "train_num_list": train_num_list,
        "train_dataset_list": train_dataset_list,
        "valid_num_list": valid_num_list,
        "valid_dataset_list": valid_dataset_list,
        "test_num_list": test_num_list,
        "test_dataset_list": test_dataset_list
    }

def merge_dataset(data_dir):
    dataset_struct = [
        ("test_num_list", "test_dataset_list", "test_feature_dataset", "test_label_dataset"),
        ("valid_num_list", "valid_dataset_list", "valid_feature_dataset", "valid_label_dataset"),
        ("train_num_list", "train_dataset_list", "train_feature_dataset", "train_label_dataset"),
    ]
    dataset_dict = load_feature_dataset(data_dir)
    merge_dict = {}
    for num_list_str, dataset_list_str, feature_dataset_str, label_dataset_str in dataset_struct:
        print dataset_list_str
        num = sum(dataset_dict[num_list_str])
        print num
        dataset_list = dataset_dict[dataset_list_str]
        # print dataset_list
        dataset = np.ndarray((num, class_num+1), dtype=np.float32)
        offset = 0
        for dataset_item in dataset_list:
            count = len(dataset_item)
            dataset[offset:offset+count, :] = dataset_item
            offset += count

        np.random.shuffle(dataset)

        feature_dataset, label_dataset = dataset[:, :class_num], dataset[:, class_num:]

        feature_dataset = normalize(feature_dataset, axis=1)
        label_dataset = (np.arange(server_type_num) == label_dataset.astype(np.int32)).astype(np.float32)
        
        print feature_dataset.shape, label_dataset.shape

        merge_dict[feature_dataset_str], merge_dict[label_dataset_str] = randomize(feature_dataset, label_dataset)
        
    return merge_dict

def save_obj(pickle_file, obj):
    try:
        with open(pickle_file, "wb") as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
    except Exception as e:
        print "Unable to save data to", pickle_file, ":", e
        raise

    statinfo = os.stat(pickle_file)
    print '%s Compressed pickle size: %.2f kb' % (pickle_file, statinfo.st_size / 1000.0)

if __name__ == "__main__":
    feature_dataset_dir = "/opt/downloads/feature_dataset/"
    merge_dict = merge_dataset(feature_dataset_dir)
    pickle_file = feature_dataset_dir + "server_dataset.pickle"
    save_obj(pickle_file, merge_dict)
    



    


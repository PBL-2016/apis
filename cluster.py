# coding: utf-8

# Getter of cluster images written by Tamamu.
# 2017-02-12

import numpy as np
import pandas as pd

csv = pd.read_csv('model_cluster.csv', dtype={'col1': 'str', 'col2': 'int'})

def get_cluster_images(cluster_number):
    return csv[csv['クラスタ']==cluster_number]['画像'].values.flatten()
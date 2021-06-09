#!/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf-8 vi:ts=4:sw=4:expandtab:ft=python
"""
/***************************************************************************
  *
  * Copyright (c) 2020 Baidu.com, Inc. All Rights Reserved
  * @file:  textmatching_predict_gpu.py
  * @date  2021/4/21 3:00 PM
  * @brief 
  *
  **************************************************************************/
"""
import paddle
import paddlehub as hub
import os
# from paddlehub.datasets import LCQMC

pwd = os.getcwd()
models_save = os.path.join(pwd, 'models_save')

data = [['这个表情叫什么', '这个猫的表情叫什么'], ['什么是智能手环', '智能手环有什么用'],
        ['介绍几本好看的都市异能小说，要完结的！', '求一本好看点的都市异能小说，要完结的'],
        ['一只蜜蜂落在日历上（打一成语）', '一只蜜蜂停在日历上（猜一成语）'],
        ['一盒香烟不拆开能存放多久？', '一条没拆封的香烟能存放多久。']]
label_map = {0: 'similar', 1: 'dissimilar'}
model = hub.Module(
    name='roberta-wwm-ext-large',
    version='2.0.2',
    task='text-matching',
    load_checkpoint=os.path.join(models_save, 'roberta-wwm-ext-large',
                                 'best_model', 'model.pdparams'),
    label_map=label_map)
results = model.predict(data, max_seq_len=128, batch_size=1, use_gpu=True)
for idx, texts in enumerate(data):
    print('TextA: {}\tTextB: {}\t Label: {}'.format(texts[0], texts[1],
                                                    results[idx]))
assert len(results) == 5
for res in results:
    if (res != 'similar') and (res != 'dissimilar'):
        raise Exception('res does not belong to similar or dissimilar, BUG!!!')

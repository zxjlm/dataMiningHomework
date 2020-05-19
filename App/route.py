# -*- coding: utf-8 -*-
__author__ = 'xiejdm'

from App import app, db, restless
from flask import render_template, jsonify, request
from App.models import HerbInfo, Diagnosis
from App.controller import get_feature, get_all_pres, get_feature_for_each_dig, km_cul
from efficient_apriori import apriori
import brewer2mpl

restless.create_api(Diagnosis, include_methods=['text'], methods=['GET', 'POST', 'DELETE', 'PATCH', 'PUT'],
                    results_per_page=10)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/num_count/')
@app.route('/num_count/<string:query_condition>')
def num_count(query_condition=None):
    '''

    :param query_condition:查询条件
    :return:渲染参数：
    '''
    pres_ll = get_all_pres()
    if query_condition is None:
        return render_template('num_count.html', data={}, elem=[], pres_dic=dict(enumerate(pres_ll)))
    else:
        res_ll, legend_data_list = get_feature(app.config['XING_LIST'], app.config['WEI_LIST'],
                                               app.config['GUIJING_LIST'], query_condition.split(','))

        return render_template('num_count.html', data={
            'object_list': [app.config['XING_LIST'], app.config['WEI_LIST'], app.config['GUIJING_LIST']],
            'legend_data_list': legend_data_list,
            'result_list': res_ll
        }, elem=['xing', 'wei', 'guijing'], pres_dic=dict(enumerate(pres_ll)))


@app.route('/components/rule', methods=['POST'])
def rules_cul():
    form = request.json
    data_raw = get_all_pres()
    # data = [data_raw[ind]['prescription'].split(';') for ind in form['data']]
    data = []
    for ind in form['data']:
        data1 = data_raw[ind].prescription
        data.append(data1.split(';'))
    items, ruless = apriori(data, min_support=float(form['supp']), min_confidence=float(form['conf']),
                            max_length=float(form['maxl']))
    item_new = {}
    for key in items.keys():
        v = {}
        for k in items[key].keys():
            v[','.join(k)] = items[key][k]
        item_new[key] = v

    rules_new = [{'name': rule.__repr__(), 'conf': rule.confidence, 'supp': rule.support, 'lift': rule.lift,
                  'conv': rule.conviction} for rule in ruless]

    nodes, nodes_tmp, links = [], [], []
    bmap = brewer2mpl.get_map('Set3', 'Qualitative', 12)
    for ind, rule in enumerate(ruless):
        if len(rule.lhs) == 1 and len(rule.rhs) == 1:
            nodes_tmp.append(rule.lhs[0])
            nodes_tmp.append(rule.rhs[0])
            links.append({'source': rule.lhs[0], 'target': rule.rhs[0], 'value': rule.confidence,
                          'lineStyle': {
                              'color': 'rgb({},{},{})'.format(bmap.colors[ind % 12][0], bmap.colors[ind % 12][1],
                                                              bmap.colors[ind % 12][2])}})
    nodes = [{'name': foo} for foo in set(nodes_tmp)]
    print(nodes)
    return render_template('content/rulesRes.html', items=item_new, rules=rules_new, nodes=nodes, links=links)


@app.route('/rules/')
def rules():
    return render_template('rules.html', pres_dic=dict(enumerate(get_all_pres())))


@app.route('/components/km', methods=['POST'])
def ap_km():
    data, legend = get_feature_for_each_dig(app.config['XING_LIST'], app.config['WEI_LIST'],
                                            app.config['GUIJING_LIST'])
    nodes, links = km_cul(data, legend, int(request.json['num']))
    return render_template('content/kmRes.html', nodes=nodes, links=links)


@app.route('/km')
def km():
    return render_template('km.html')

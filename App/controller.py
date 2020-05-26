from brewer2mpl import brewer2mpl
from flask import g

from App.models import Diagnosis, HerbInfo


def get_all_pres():
    return Diagnosis.query.with_entities(Diagnosis.id, Diagnosis.province, Diagnosis.prescription).all()


def get_feature(ll_xing, ll_wei, ll_guijing, ll_query_condition):
    diagnosis_list = Diagnosis.query.filter(Diagnosis.id.in_(ll_query_condition)).all()
    xing_result_list, wei_result_list, guijing_result_list = list(), list(), list()
    legend_data_list = list()
    for diagnosis in diagnosis_list:
        object_dic = {
            'xing': dict(zip(ll_xing, [0] * len(ll_xing))),
            'wei': dict(zip(ll_wei, [0] * len(ll_wei))),
            'guijing': dict(zip(ll_guijing, [0] * len(ll_guijing)))
        }
        legend_data_list.append(str(diagnosis.id) + diagnosis.province)
        herb_list = diagnosis.prescription.split(';')
        feature_counter_res, _ = feature_counter(object_dic, herb_list, False)

        xing_result_list.append(list(feature_counter_res['xing'].values()))
        wei_result_list.append(list(feature_counter_res['wei'].values()))
        guijing_result_list.append(list(feature_counter_res['guijing'].values()))
    return [xing_result_list, wei_result_list, guijing_result_list], legend_data_list


def feature_counter(object_dic, ll_herb, stat=True):
    unfind = []
    for herb in ll_herb:
        herb_info = HerbInfo.query.filter(HerbInfo.name == herb).first()
        if herb_info:
            for obj in object_dic.keys():
                obj_feature_res = getattr(herb_info, obj)
                if obj_feature_res:
                    for feature in getattr(herb_info, obj).split('、'):
                        if stat:
                            object_dic[obj][feature] += 1 / len(ll_herb)
                        else:
                            object_dic[obj][feature] += 1
        else:
            unfind.append(herb)
    return object_dic, unfind


def get_feature_for_each_dig(ll_xing, ll_wei, ll_guijing):
    diagnosis_list = Diagnosis.query.all()
    legend_data_list = list()
    diagnosis_res_list = []
    for diagnosis in diagnosis_list:
        object_dic = {
            'xing': dict(zip(ll_xing, [0] * len(ll_xing))),
            'wei': dict(zip(ll_wei, [0] * len(ll_wei))),
            'guijing': dict(zip(ll_guijing, [0] * len(ll_guijing)))
        }
        legend_data_list.append(str(diagnosis.id) + diagnosis.province)
        herb_list = diagnosis.prescription.split(';')
        feature_counter_res, _ = feature_counter(object_dic, herb_list)
        diagnosis_res_list.append(
            list(feature_counter_res['xing'].values()) + list(feature_counter_res['wei'].values()) +
            list(feature_counter_res['guijing'].values()))
    return diagnosis_res_list, legend_data_list


def classif_heandler(data, ll_xing, ll_wei, ll_guijing):
    import pickle
    object_dic = {
        'xing': dict(zip(ll_xing, [0] * len(ll_xing))),
        'wei': dict(zip(ll_wei, [0] * len(ll_wei))),
        'guijing': dict(zip(ll_guijing, [0] * len(ll_guijing)))
    }
    herb_list = data.split(';')
    feature_counter_res, unfind = feature_counter(object_dic, herb_list)
    with open('kmeans_fit.pkl', 'rb') as file:
        kmeans = pickle.load(file)
    return kmeans.predict([list(feature_counter_res['xing'].values()) + list(feature_counter_res['wei'].values()) +
                           list(feature_counter_res['guijing'].values())]), kmeans.labels_, unfind


def km_cul(data, legend_list, clusters_num=7):
    from sklearn.cluster import KMeans
    import pickle
    labels_dict = {}
    bmap = brewer2mpl.get_map('Set3', 'Qualitative', 12)
    kmeans = KMeans(n_clusters=clusters_num, random_state=0)
    kmeans_fit = kmeans.fit(data)
    labels = kmeans_fit.labels_
    with open('kmeans_fit.pkl', 'wb') as file:
        pickle.dump(kmeans, file)
    # legend_dict = [{v: labels[k]} for k, v in enumerate(legend_list)]
    ind_cluster_list, links, nodes = [], [], [{'name': foo} for foo in legend_list]
    for ind in range(clusters_num):
        for ind1, label in enumerate(labels):
            if ind == label:
                ind_cluster_list.append(ind1)
                continue

    for ind, label in enumerate(labels):
        if label in list(labels_dict.keys()):
            labels_dict[label].append(ind)
        else:
            labels_dict[label] = [ind]
        if legend_list[ind_cluster_list[label]] == legend_list[ind]:
            continue
        links.append({'source': legend_list[ind_cluster_list[label]], 'target': legend_list[ind],
                      'lineStyle': {
                          'color': 'rgb({},{},{})'.format(bmap.colors[label % 12][0], bmap.colors[label % 12][1],
                                                          bmap.colors[label % 12][2])}})

    return nodes, links, labels_dict


def my_map(ll, num):
    import numpy as np
    return list(np.array(ll) / num)

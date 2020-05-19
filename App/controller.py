from brewer2mpl import brewer2mpl

from App.models import Diagnosis, HerbInfo


def get_all_pres():
    return Diagnosis.query.with_entities(Diagnosis.id, Diagnosis.prescription).all()


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
        feature_counter_res = feature_counter(object_dic, herb_list)

        xing_result_list.append(list(feature_counter_res['xing'].values()))
        wei_result_list.append(list(feature_counter_res['wei'].values()))
        guijing_result_list.append(list(feature_counter_res['guijing'].values()))
    return [xing_result_list, wei_result_list, guijing_result_list], legend_data_list


def feature_counter(object_dic, ll_herb):
    for herb in ll_herb:
        herb_info = HerbInfo.query.filter(HerbInfo.name == herb).first()
        if herb_info:
            for obj in object_dic.keys():
                obj_feature_res = getattr(herb_info, obj)
                if obj_feature_res:
                    for feature in getattr(herb_info, obj).split('、'):
                        object_dic[obj][feature] += 1
        else:
            continue
    return object_dic


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
        feature_counter_res = feature_counter(object_dic, herb_list)
        diagnosis_res_list.append(
            list(feature_counter_res['xing'].values()) + list(feature_counter_res['wei'].values()) +
            list(feature_counter_res['guijing'].values()))
    return diagnosis_res_list, legend_data_list


def km_cul(data, legend_list, clusters_num=7):
    from sklearn.cluster import KMeans
    bmap = brewer2mpl.get_map('Set3', 'Qualitative', 12)
    kmeans = KMeans(n_clusters=clusters_num, random_state=0).fit(data)
    labels = kmeans.labels_
    # legend_dict = [{v: labels[k]} for k, v in enumerate(legend_list)]
    ind_cluster_list, links, nodes = [], [], [{'name': foo} for foo in legend_list]
    for ind in range(clusters_num):
        for ind1, label in enumerate(labels):
            if ind == label:
                ind_cluster_list.append(ind1)
                continue

    for ind, label in enumerate(labels):
        if legend_list[ind_cluster_list[label]] == legend_list[ind]:
            continue
        links.append({'source': legend_list[ind_cluster_list[label]], 'target': legend_list[ind],
                      'lineStyle': {
                          'color': 'rgb({},{},{})'.format(bmap.colors[label % 12][0], bmap.colors[label % 12][1],
                                                          bmap.colors[label % 12][2])}})
    return nodes, links

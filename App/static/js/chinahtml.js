// 国内数据
var chinaData = null;
$.when($.ajax({
        url: "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5",
        dataType: "jsonp",
        success: function(data) {
            pastchinaData = JSON.parse(data.data);
        }
    }), $.ajax({
        url: "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5",
        dataType: "jsonp",
        success: function(data) {
            chinaData = JSON.parse(data.data);
        }
    })).then(function() {
        // 更新标题
        title();
        // 注入总览数据
        brief();
        // 疫情地图
        map();


    })
    // 标题
function title() {

    $(".brief .brief_header p").text("更新时间 - " + chinaData.lastUpdateTime)
}
// 注入总览数据
function brief() {
    // 拼接字符串
    var htmlStr = `
            <li class="allConfirm">
                <div class="number">${chinaData.chinaTotal.confirm}</div>
                <div class="item">累计确诊</div>
                <div class="change"><span>昨日</span><b>+${chinaData.chinaAdd.confirm}</b></div>
            </li>
            <li class="nowConfirm">
                <div class="number">${chinaData.chinaTotal.nowConfirm}</div>
                <div class="item">现有确诊</div>
                <div class="change"><span>昨日</span><b>+${chinaData.chinaAdd.nowConfirm}</b></div>
            </li>
            <li class="deadNum">
                <div class="number">${chinaData.chinaTotal.dead}</div>
                <div class="item">死亡人数</div>
                <div class="change"><span>昨日</span><b>+${chinaData.chinaAdd.dead}</b></div>
            </li>
            <li class="cureNum">
                <div class="number">${chinaData.chinaTotal.heal}</div>
                <div class="item">治愈人数</div>
                <div class="czhange"><span>昨日</span><b>+${chinaData.chinaAdd.heal}</b></div>
            </li>
        `;
    // 设置字符串为HTML内容
    $(".brief_body").html(htmlStr);
}
// 疫情地图
function map() {
    var virusDatas = [];
    // 遍历数据，获取目标信息
    // $.each(foreignData.foreignList, function(i, v) {
    //     virusDatas[i] = {};
    //     virusDatas[i].name = v.name;
    //     virusDatas[i].value = v.confirm;
    // })
    // 加入中国数据
    $.each(chinaData.areaTree[0].children, function(i, v) {
        virusDatas[i] = {};
        virusDatas[i].name = v.name;
        virusDatas[i].value = v.total.confirm;
    })
    var myChart = echarts.init(document.querySelector(".brief .map_info"));
    // 指定图表的配置项和数据
    option = {
        title: {
            text: '中国疫情图',
            left: 'center'
        },
        tooltip: {
            trigger: 'item'
        },
        legend: {
            orient: 'vertical',
            left: 'left',
            data: ['中国疫情图']
        },
        visualMap: {

            pieces: [
                { min: 1000, max: 1000000, label: '大于等于1000人', color: '#e2482b' },
                { min: 500, max: 999, label: '确诊500-999人', color: '#fe5e3b' },
                { min: 100, max: 499, label: '确诊100-499人', color: '#ff7c20' },
                { min: 10, max: 99, label: '确诊10-99人', color: '#ffc24b' },
                { min: 1, max: 9, label: '确诊1-9人', color: '#fff7ba' },

            ],
        },
        toolbox: {
            show: true,
            orient: 'vertical',
            left: 'right',
            top: 'center',
            feature: {
                mark: { show: true },
                dataView: { show: true, readOnly: false },
                restore: { show: true },
                saveAsImage: { show: true }
            }
        },
        series: [{
            showLegendSymbol: false,
            name: '确诊数',
            type: 'map',
            mapType: 'china',
            itemStyle: {
                emphasis: {
                    label: {
                        show: false
                    }
                }
            },
            data: virusDatas,

        }]
    };

    //使用指定的配置项和数据显示图表
    myChart.setOption(option);
    $(".brief .map_tab span").eq(0).click(function() { fn("confirm") });
    $(".brief .map_tab span").eq(1).click(function() { fn("nowConfirm") });

    function fn(valueName) {
        $.each(chinaData.areaTree[0].children, function(i, v) {
            // virusDatas[i].value = v[valueName];
            virusDatas[i] = {};
            virusDatas[i].name = v.name;
            virusDatas[i].value = v.total[valueName];
        })
        option.series[0].data = virusDatas;
        myChart.setOption(option);
    }
    $(".map_tab span").click(function() {
        $(this).addClass("cur").siblings().removeClass("cur");
    })
}
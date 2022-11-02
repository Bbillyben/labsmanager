var dataFrameLossCard;
var lossChart;
function dblosscard_initCard(dataF){
    dataFrameLossCard=dataF;

    // add listener
    dblosscard_addBtnListener();

    datasets=createDataSet(dataFrameLossCard, "type", "end_date", "amount");
    dblosscard_updateGraph(datasets);
}
function dblosscard_addBtnListener(){
    $('#db_losscard_radio_type .radiotab').each(function(){
        $(this).on('change, click', dblosscard_radioListener);
    })
}


function dblosscard_radioListener(e){
    var typeG=$(this).attr('id').replace('tab', '').toLowerCase();
    var csrftoken = getCookie('csrftoken');
    
    //console.log("dblosscard_radioListener type :"+typeG)
    datasets=createDataSet(dataFrameLossCard, typeG, "end_date", "amount");
    dblosscard_updateGraph(datasets);
}


function dblosscard_updateGraph(data){
    if(lossChart)lossChart.destroy();
    const dataset = {
        datasets: data
      };


var ctx = document.getElementById('canvas').getContext('2d');
lossChart = new Chart(ctx , {
    type: "line",
    data: dataset, 
    options: {
      responsive: true,
      scales: {
        x: {
          type:'time',
          parsing:'false',      
        },
        y: {
            stacked: true,
            title: {
              display: true,
              text: 'Value'
            }
          }
      }
    }
  });
}

// {"schema":{"fields":[{"name":"project","type":"string"},{"name":"funder","type":"string"},{"name":"type","type":"string"},{"name":"end_date","type":"string"},{"name":"amount","type":"string"}],"primaryKey":["project","funder","type","end_date"],"pandas_version":"1.4.0"},"data":[{"project":"Ripolinette","funder":"FRM","type":"EQUIP","end_date":"2021-12-31T00:00:00.000","amount":12500.0},{"project":"Roupette","funder":"FRM","type":"FCT","end_date":"2022-12-31T00:00:00.000","amount":100000.0},{"project":"PreciNASH","funder":"ANR","type":"FCT","end_date":"2023-08-31T00:00:00.000","amount":-110000.0},{"project":"PreciNASH","funder":"ANR","type":"FG","end_date":"2023-08-31T00:00:00.000","amount":12800.0},{"project":"PreciNASH","funder":"ANR","type":"RH CDD","end_date":"2023-08-31T00:00:00.000","amount":280000.0}]} 
function createDataSet(datas, setLabel, setXAxis, setAmount){
    var datasets=[];
    var indexDict={}
    if(setLabel in datas.schema.primaryKey){
        //console.log(setLabel + " not in datas ");
        return null;
    }
    var i=0;
    var ds;
    var seq = palette('cb-Pastel1', datas.data.length);
  // cb-Paired cb-Pastel1
    for (var item in datas.data) {
        d=datas.data[item];
        // get the data set
        if(d[setLabel] in indexDict){
            id=indexDict[d[setLabel] ];
            ds=datasets[id];
        }else{
            indexDict[d[setLabel]]=i;
            i+=1;
            ds={
                label: d[setLabel],
                data: [],
                backgroundColor: "#"+seq[i], 
                fill: true
            };
            datasets.push(ds);
            
        }
        // get the value
        id=getIndexOf(d[setXAxis], ds.data,'x');
        cAmount= Math.abs(d[setAmount])
        if( id == -1){
            ds.data.push({x:d[setXAxis], y:cAmount});
        }else{
            v=ds.data[id];
            v.y+=cAmount;
            ds.data[id]=v;
        }
     }
     //console.log("dataset :"+datasets);
     // sort et cumul 
     for(var ds in datasets){
        item=datasets[ds]
        item.data = item.data.sort(compareDatasetDate);
        curr=0;
        for(i = 0 ; i< item.length; i++){
            curr= item.data['y']+curr;
            item.data['y']=curr;
        }
        datasets[ds]=item
     }
     //console.log(datasets);
     return datasets;
    
}

function getIndexOf(key, arr, arrKey){
    for (i = 0; i < arr.length ; i++) { 
        if(arr[i][arrKey] == key)return i;
    }
    return -1;
}
function compareDatasetDate(a, b){
    if ( a.x < b.x ){
        return -1;
    }
    if ( a.x > b.x ){
        return 1;
    }
    return 0;
}


let historyChart = null;

function getRankBadge(rank) {


    if(rank === 1)
        return "🥇 TOP 1";


    if(rank === 2)
        return "🥈 TOP 2";


    if(rank === 3)
        return "🥉 TOP 3";


    return "#" + rank;

}



function getSignal(signal) {


    if(signal === "MAINTAIN")
        return "🟢 유지";


    if(signal === "BUY")
        return "🚀 매수";


    if(signal === "SELL")
        return "🔴 매도";


    return signal;

}



function getGradeBadge(grade){


    if(grade === "A")
        return "🟢 A";


    if(grade === "B")
        return "🟡 B";


    if(grade === "C")
        return "🟠 C";


    return "🔴 " + grade;

}



function loadDashboard(){


    fetch("/api/ranking")

    .then(response => response.json())

    .then(result => {


        const dashboard =
            document.getElementById(
                "dashboard"
            );


        const summary =
        document.getElementById(
            "summary"
        );


        summary.innerHTML =

        `
        <div class="summary-card">


        <h3>
        📊 Market Summary
        </h3>


        <p>
        Ranking Count :
        <b>
        ${result.count}
        </b>
        </p>


        <p>
        Top ETF :
        <b>
        ${result.data[0].ticker}
        </b>
        </p>


        <p>
        Signal :
        <b>
        ${getSignal(
        result.data[0].prediction
        )}
        </b>
        </p>


        </div>
        `;    


        dashboard.innerHTML = "";


        result.data.forEach(item => {


            const card =
                document.createElement(
                    "div"
                );


            card.className =
                "card";

            card.onclick = function(){

                loadHistory(
                    item.ticker
                );

            };    


            card.innerHTML =

            `
            <h2>
            ${getRankBadge(item.rank)}
            ${item.ticker}
            </h2>


            <div class="score-box">

            <p>
            Score
            </p>

            <div class="bar">

            <div class="score-fill"
            style="width:${item.score}%">

            </div>

            </div>

            <b>${item.score}</b>

            </div>



            <div class="score-box">

            <p>
            Enhanced
            </p>

            <div class="bar">

            <div class="score-fill enhanced"
            style="width:${item.enhanced_score}%">

            </div>

            </div>

            <b>${item.enhanced_score}</b>

            </div>


            <p>
            Grade :
            ${getGradeBadge(item.grade)}
            </p>


            <p>
            Signal :
            <span class="signal">
            ${getSignal(item.prediction)}
            </span>
            </p>


            <p>
            Stability :
            ${item.stability}
            </p>

            <div class="insight">


            <h3>
            🤖 AI Insight
            </h3>


            <p>
            판단 :
            <b>
            ${getSignal(item.prediction)}
            </b>
            </p>


            <p>
            안정성 :
            ${item.stability}
            </p>


            <p>
            Bonus :
            ${item.prediction_bonus}
            </p>


            <p>
            투자 의견 :
            <b>
            Stable Holding
            </b>
            </p>


            </div>

            `;


            card.onclick = function(){

                loadHistory(item.ticker);

            };


            dashboard.appendChild(card);


        });


         loadHistory(
            result.data[0].ticker
        );



    })

    .catch(error => {

        console.error(
            "Dashboard API Error",
            error
        );

    });


}



// 최초 실행

loadDashboard();



// 10초마다 갱신

setInterval(
    loadDashboard,
    10000
);



async function loadHistory(ticker){


    const response =
    await fetch(
        `/api/history/${ticker}`
    );


    const result =
    await response.json();


    const labels =
    result.history.map(
        x => x.date
    );


    const scores =
    result.history.map(
        x => x.score
    );


    const ctx =
    document
    .getElementById(
        "historyChart"
    );


    if(historyChart){

    historyChart.destroy();

    }


    historyChart = new Chart(
        ctx,
        {
            type:"line",

            data:{
                labels:labels,

                datasets:[
                    {
                        label:
                        "Score",

                        data:scores
                    }
                ]
            }
        }
    );
}
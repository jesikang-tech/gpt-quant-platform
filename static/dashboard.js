let historyChart = null;

let portfolioMode = "balanced";


function getRecommendationIcon(signal){


    if(signal === "BUY")
        return "🟢";


    if(signal === "SELL")
        return "🔴";


    if(signal === "MAINTAIN")
        return "🟡";


    return "⚪";

}


function getConfidenceIcon(confidence){


    if(confidence === "HIGH")
        return "🟢";


    if(confidence === "MEDIUM")
        return "🟡";


    if(confidence === "LOW")
        return "⚪";


    return "⚪";

}


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


        const topTicker =
            result.data[0].ticker;


        return Promise.all([

            result,


            fetch("/api/intelligence")
                .then(response => response.json()),


            fetch(
                "/api/recommendation/"
                + topTicker
            )
                .then(response => response.json())

        ]);


    })


    .then(
    ([result, intelligence, recommendationData]) => {


        const dashboard =
            document.getElementById(
                "dashboard"
            );


        const topTicker =
            result.data[0].ticker;
        
            
    
        
        const summary =
        document.getElementById(
            "summary"
        );


        console.log(
            "RESULT:",
            result
        );

        console.log(
            "INTELLIGENCE:",
            intelligence
        );

        console.log(
            "RECOMMENDATION:",
            recommendationData
        );


        summary.innerHTML =

        `
        <div class="summary-card">


        <div class="intelligence-title">
        GPT ETF Intelligence
        </div>


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


        <div class="intelligence-score">

        AI Score :

        <b>
        ${intelligence.score}
        </b>

        </div>


        <p>
        Grade :
        <b>
        ${intelligence.grade}
        </b>
        </p>


        <div class="recommendation-box">

        <div class="recommendation-title">

        🤖 AI Recommendation

        </div>


        <div class="recommendation-signal ${
        recommendationData.recommendation.recommendation.toLowerCase()
        }">

        ${getRecommendationIcon(
        recommendationData.recommendation.recommendation
        )}

        ${recommendationData.recommendation.recommendation}

        </div>


        <div class="recommendation-confidence">

        Confidence

        <br>

        <b>

        ${getConfidenceIcon(
        recommendationData.recommendation.confidence
        )}

        ${recommendationData.recommendation.confidence}

        </b>

        </div>


        <div class="recommendation-reasons">

        <div class="reason-title">

        📊 AI Analysis Reasons

        </div>


        <div class="reason-item">

        📈 Score Analysis

        <br>

        ✓ ${recommendationData.recommendation.reasons[0]}

        </div>



        <div class="reason-item">

        📊 Ranking Analysis

        <br>

        ✓ ${recommendationData.recommendation.reasons[1]}

        </div>



        <div class="reason-item">

        🛡 Risk Analysis

        <br>

        ✓ ${recommendationData.recommendation.reasons[2]}

        </div>


        </div>


        </div>


       <div class="intelligence-opinion">


        🤖 GPT Analyst

        <br><br>


        ${intelligence.opinion}


        </div>


        </div>


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

            
            console.log(
                "CARD CREATED :",
                item.ticker
            );


            card.onclick = function(){

                console.log(
                    "CLICK ETF :",
                    item.ticker
                );


                loadDetail(
                    item.ticker
                );


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
            📈 Return Score :
            <b>
            ${item.return_score}
            </b>
            </p>


            <p>
            📊 Trend Score :
            <b>
            ${item.trend_score}
            </b>
            </p>


            <p>
            📐 Slope Score :
            <b>
            ${item.slope_score}
            </b>
            </p>


            <p>
            🎯 Final Score :
            <b>
            ${item.final_score}
            </b>
            </p>


            <p>
            Stability :
            ${item.stability}
            </p>

            <div class="insight">


            <h3>
            🤖 GPT Quant AI Insight
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

loadPortfolioAdvisor();


// 10초마다 갱신

setInterval(
    loadDashboard,
    10000
);


setInterval(
    loadPortfolioAdvisor,
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


    const ranks =
    result.history.map(
        x => x.rank
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

                        data:scores,

                        yAxisID:
                        "y"
                    },


                    {
                        label:
                        "Rank",

                        data:ranks,

                        yAxisID:
                        "y1"
                    }
                ]
            },

            options:{
                scales:{

                    y:{
                        beginAtZero:true,
                        max:100,
                        position:"left",
                        title:{
                            display:true,
                            text:"Score"
                        }
                    },


                    y1:{
                        beginAtZero:true,
                        reverse:true,
                        position:"right",
                        title:{
                            display:true,
                            text:"Rank"
                        }
                    }

                }
            }
        }
    );
}



async function loadDetail(ticker){

    const response =
    await fetch(
        `/api/detail/${ticker}`
    );


    const result =
    await response.json();


    const panel =
    document.getElementById(
        "detail-content"
    );


    panel.innerHTML =

    `
    <h3>
    ${result.ticker}
    </h3>


    <p>
    Score :
    <b>${result.score}</b>
    </p>


    <p>
    Enhanced :
    <b>${result.enhanced_score}</b>
    </p>


    <h3>
    🤖 AI Intelligence
    </h3>


    <p>
    📈 Return Score :
    <b>${result.return_score}</b>
    </p>


    <p>
    📊 Trend Score :
    <b>${result.trend_score}</b>
    </p>


    <p>
    📐 Slope Score :
    <b>${result.slope_score}</b>
    </p>


    <p>
    🎯 Final Score :
    <b>${result.final_score}</b>
    </p>


    <p>
    Grade :
    ${getGradeBadge(result.grade)}
    </p>


    <p>
    Signal :
    ${getSignal(result.prediction)}
    </p>


    <p>
    Stability :
    ${result.stability}
    </p>
    
    <hr>

    <p>
    🤖 AI Insight
    </p>

    <p>
    📈 Trend :
    ${result.analysis.trend}
    </p>

    <p>
    ⚠ Risk :
    ${result.analysis.risk}
    </p>

    <p>
    💡 Opinion :
    ${result.analysis.opinion}
    </p>

    <p>
    📊 Score Momentum :
    ${result.analysis.score_change}
    </p>


    <p>
    🔮 Prediction :
    ${result.analysis.prediction}
    </p>

    `;
}


function changePortfolioMode(mode){

    portfolioMode = mode;

    loadPortfolioAdvisor();

}


async function loadPortfolioAdvisor(){

    const response =
    await fetch(
        "/api/portfolio?mode=" + portfolioMode
    );


    const result =
    await response.json();


    const panel =
    document.getElementById(
        "portfolio-content"
    );


     let html = "";


    html += `

    <h3>
    Strategy :
    ${result.strategy}
    </h3>

    `;


    result.portfolio.forEach(item => {


        let cashClass = "";

        if(item.ticker === "CASH"){
            cashClass = "portfolio-cash";
        }


        html += `


        <div class="portfolio-card ${cashClass}">


            <div class="ticker">

            ${item.ticker}

            </div>



            <div class="portfolio-weight">

            Weight :
            <b>
            ${item.weight}%
            </b>

            </div>



            <div class="portfolio-score">

            Score :
            <b>
            ${item.score ?? "-"}
            </b>

            </div>



            <div class="portfolio-reason">

            ${item.reason}

            </div>


        </div>


        `;


    });


    html += `


    <div class="portfolio-insight">


        <h3>
        🧠 GPT Portfolio Insight
        </h3>



        <p>

        📌 Summary

        <br>

        <b>
        ${result.insight.summary}
        </b>

        </p>



        <p>

        🧠 AI Opinion

        <br>

        ${result.insight.opinion}

        </p>


    </div>


    `;


    panel.innerHTML = html;


   
}



let currentPortfolioMode = "balanced";


function changePortfolioMode(mode){

    portfolioMode = mode;

    currentPortfolioMode = mode;

    loadPortfolioAdvisor();

}
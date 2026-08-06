let historyChart = null;

let portfolioMode = "balanced";

let portfolioAnalytics = null;


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

console.log("BEFORE PORTFOLIO HISTORY");

loadPortfolioAdvisor();

loadPortfolioHistory();

loadMarketCondition();

loadMarketRegime();

loadMarketStrategy();

loadAIDecision();

loadAIDecisionSummary();

loadAIDecisionQuality();

loadAIDecisionTrend();

loadAIDecisionChart();

loadAIDecisionStatistics();

loadAIDecisionPerformance();

loadAIDecisionReliability();

loadAIAdaptiveStrategy();

loadAIRebalance();

loadAIOptimization();

loadAIDecisionHistory();


// 10초마다 갱신

setInterval(
    loadDashboard,
    10000
);


setInterval(
    loadPortfolioAdvisor,
    10000
);


setInterval(
    loadMarketRegime,
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



async function loadPortfolioAdvisor(save=false){

    const response =
     await fetch(
        "/api/portfolio?mode="
        + portfolioMode
        + "&save="
        + save
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




    let healthColor = "#e74c3c";

    if(result.intelligence.health_score >= 90){

        healthColor = "#27ae60";

    }
    else if(result.intelligence.health_score >= 80){

        healthColor = "#f39c12";

    }


    let confidenceColor = "#f39c12";

    if(result.intelligence.confidence === "HIGH"){

        confidenceColor = "#27ae60";

    }
    else if(result.intelligence.confidence === "LOW"){

        confidenceColor = "#e74c3c";

    }



    let riskColor = "#f39c12";

    if(
        result.intelligence.risk_level === "Low Risk"
        ||
        result.intelligence.risk_level === "Balanced"
    ){
        riskColor = "#27ae60";
    }
    else if(result.intelligence.risk_level === "High Risk"){
        riskColor = "#e74c3c";
    }



    html += `


    <div class="portfolio-intelligence">


        <h3>
        🤖 GPT Portfolio Intelligence
        </h3>


        <p>
        ❤️ Health Score
        <br>

        <span
        style="
        background:${healthColor};
        color:white;
        padding:4px 12px;
        border-radius:12px;
        font-weight:bold;
        "
        >
        ${result.intelligence.health_score} / 100
        </span>

        </p>



        <p>
        🛡 Risk Level
        <br>

        <span
        style="
        background:${riskColor};
        color:white;
        padding:4px 12px;
        border-radius:12px;
        font-weight:bold;
        "
        >
        ${result.intelligence.risk_level}
        </span>

        </p>



        <p>
        🔥 Confidence
        <br>

        <span
        style="
        background:${confidenceColor};
        color:white;
        padding:4px 12px;
        border-radius:12px;
        font-weight:bold;
        "
        >
        ${result.intelligence.confidence}
        </span>

        </p>



        <p>
        💰 Cash Weight
        <br>
        <b>
        ${result.intelligence.cash_weight}%
        </b>
        </p>



        <p>
        📊 Allocation
        <br>

        ${
            Object.entries(
                result.intelligence.allocation
            )
            .map(
                item =>
                item[0]
                +
                " : "
                +
                item[1]
                +
                "%"
            )
            .join("<br>")
        }

        </p>



        <p>
        🌎 Market Regime
        <br>

        <b>
        ${result.insight.analytics.market_regime}
        </b>

        </p>


        <p>
        📈 Market Strength
        <br>

        <b>
        ${result.insight.analytics.market_strength}
        </b>

        </p>


        <p>
        🎯 Market Confidence
        <br>

        <b>
        ${result.insight.analytics.market_confidence}%
        </b>

        </p>



        <p>
        🔄 AI Rebalance
        <br>

        ${result.intelligence.rebalance}

        </p>


    </div>


    `;


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


         <p>

        📊 Average Score

        <br>

        <b>
        ${result.insight.analytics.average_score}
        </b>

        </p>



        <p>

        🏆 Top ETF

        <br>

        <b>
        ${result.insight.analytics.top_etf}
        </b>

        (
        ${result.insight.analytics.top_score}
        )

        </p>



        <p>

        🛡 Diversification

        <br>

        <b>
        ${result.insight.analytics.diversification}
        </b>

        </p>



        <p>

        💰 Cash Weight

        <br>

        <b>
        ${result.insight.analytics.cash_weight}%
        </b>

        </p>


    </div>


    `;


    

    panel.innerHTML = html;




    loadPortfolioAnalytics();
   
}



let currentPortfolioMode = "balanced";


function changePortfolioMode(mode){

     portfolioMode = mode;

    currentPortfolioMode = mode;

    loadPortfolioAdvisor(true);

}



async function loadPortfolioHistory(){

    const response =
    await fetch(
        "/api/portfolio/history"
    );


    const result =
    await response.json();


    console.log(
        "PORTFOLIO HISTORY:",
        result.history
    );


    const panel =
    document.getElementById(
        "portfolio-history"
    );


    let html = "";


    html += `

    <h3>
    📌 Portfolio History
    </h3>

    `;


    result.history.forEach(item => {


        html += `

        <div class="history-card">


        <b>
        ${item.mode.toUpperCase()}
        </b>


        <br>


        ETF :
        ${item.ticker}


        <br>


        Weight :
        ${item.weight}%


        <br>


        Score :
        ${item.score ?? "-"}


        <br>


        Reason :
        ${item.reason}


        <br>


        Health Score :
        ${item.health_score ?? "-"}


        <br>


        Confidence :
        ${item.confidence ?? "-"}


        <br>


        Market Condition :
        ${item.market_condition ?? "-"}


        <br>


        ${item.created_at}


        </div>

        `;


    });

    panel.innerHTML = html;
    

}



async function loadPortfolioAnalytics(){

    const response =
    await fetch(
        "/api/portfolio/analytics"
    );


    const result =
    await response.json();


    const panel =
    document.getElementById(
        "portfolio-analytics"
    );


    const analytics =
    result.analytics;


    let html = "";


    html += `

    <div class="analytics-card">

    <h3>
    📊 Portfolio Analytics
    </h3>


    <p>
    Total Decisions :
    <b>
    ${analytics.total_history}
    </b>
    </p>


    <p>
    📌 Last Saved AI Strategy :
    <br>
    <b>
    ${analytics.latest_mode.toUpperCase()}
    </b>
    </p>


    <p>
    🎯 Current View Strategy :
    <br>
    <b>
    ${portfolioMode.toUpperCase()}
    </b>
    </p>


    <h4>
    Strategy Usage
    </h4>

    `;


    analytics.mode_analysis.forEach(item => {

        const width =
        Math.min(
            item[1] / analytics.total_history * 100,
            100
        );


        html += `

        <div class="analytics-bar-row">

            <div class="analytics-label">
                ${item[0].toUpperCase()}
            </div>


            <div class="analytics-bar">

                <div class="analytics-fill"
                style="width:${width}%">

                </div>

            </div>


            <div class="analytics-value">
                ${item[1]} times
            </div>


        </div>

        `;

    });



    html += `

    <h4>
    Average Allocation
    </h4>

    `;


    analytics.weight_analysis.forEach(item => {


        html += `


        <div class="analytics-bar-row">


            <div class="analytics-label">
                ${item[0]}
            </div>



            <div class="analytics-bar">


                <div class="analytics-fill"
                style="width:${item[1]}%">

                </div>


            </div>



            <div class="analytics-value">

                ${item[1].toFixed(2)}%

            </div>


        </div>


        `;


    });


    html += `

    </div>

    `;


    panel.innerHTML = html;

}



async function loadMarketCondition(){

    const response =
    await fetch(
        "/api/portfolio/market-condition"
    );


    const result =
    await response.json();


    const panel =
    document.getElementById(
        "market-condition"
    );


    const market =
    result.market_condition;


    panel.innerHTML =

    `
    <div class="market-card">


        <h3>
        GPT Market Intelligence
        </h3>


        <p>
        Market Condition :
        <b>
        ${market.market}
        </b>
        </p>


        <p>
        Average Score :
        <b>
        ${market.average_score}
        </b>
        </p>


        <p>
        Confidence :
        <b>
        ${market.confidence}
        </b>
        </p>


        <p>
        Recommended Strategy :
        <b>
        ${market.recommended_mode}
        </b>
        </p>


    </div>
    `;

}



async function loadMarketRegime(){

    const response =
    await fetch(
        "/api/market-regime"
    );

    const result =
    await response.json();

    const panel =
    document.getElementById(
        "market-regime-content"
    );

    let regimeColor = "#f1c40f";

    if(result.regime === "BULLISH"){

        regimeColor = "#27ae60";

    }
    else if(result.regime === "BEARISH"){

        regimeColor = "#e74c3c";

    }

    panel.innerHTML =

    `
    <div class="market-regime-card">

        <h3>

        <span
        style="
        background:${regimeColor};
        color:white;
        padding:4px 12px;
        border-radius:12px;
        font-weight:bold;
        "
        >
        ${result.regime}
        </span>

        </h3>

        <p>
        🎯 Confidence :
        <b>${result.confidence}%</b>
        </p>

        <p>
        📈 Average Score :
        <b>${result.avg_score}</b>
        </p>

        <p>
        🏆 Highest Score :
        <b>${result.max_score}</b>
        </p>

        <p>
        📉 Lowest Score :
        <b>${result.min_score}</b>
        </p>

        <p>
        📊 Score Spread :
        <b>${result.score_spread}</b>
        </p>

        <p>
        💪 Market Strength :
        <b>${result.market_strength}</b>
        </p>

        <p>
        📌 Breadth :
        <b>${result.breadth}</b>
        </p>

        <p>
        ⚠ Risk :
        <b>${result.risk}</b>
        </p>

        <p>
        💡 Strategy :
        <b>${result.strategy}</b>
        </p>

    </div>
    `;

}



async function loadMarketStrategy(){

    const response =
    await fetch(
        "/api/market-strategy"
    );


    const result =
    await response.json();


    const panel =
    document.getElementById(
        "market-strategy"
    );



    let strategyColor = "#3498db";

    if(result.portfolio_mode === "aggressive"){

        strategyColor = "#e74c3c";

    }
    else if(result.portfolio_mode === "conservative"){

        strategyColor = "#27ae60";

    }


    panel.innerHTML =

    `
    <div class="market-strategy-card">


        <h3>
        🧠 AI Market Strategy
        </h3>


        <p>
        Strategy :
        <b>
        ${result.strategy}
        </b>
        </p>


        <p>
        Portfolio Mode :
        <span
        style="
        background:${strategyColor};
        color:white;
        padding:4px 10px;
        border-radius:12px;
        font-weight:bold;
        "
        >
        ${result.portfolio_mode.toUpperCase()}
        </span>
        </p>


        <p>
        Cash Target :
        <b>
        ${result.cash_target}%
        </b>
        </p>


        <p>
        Recommendation :
        <b>
        ${result.recommendation}
        </b>
        </p>


        <p>
        Market Strength :
        <b>
        ${result.market_strength}
        </b>
        </p>


        <p>
        Confidence :
        <b>
        ${result.confidence}%
        </b>
        </p>


        <p>
        Rebalance Action :
        <b>
        ${result.rebalance_action}
        </b>
        </p>

        <p>
        💡 AI Message
        <br>
        ${result.message}
        </p>


    </div>
    `;

}



async function loadAIDecision(){

    const response =
    await fetch(
        "/api/ai-decision"
    );


    const result =
    await response.json();


    const decision =
    result.decision;


    const panel =
    document.getElementById(
        "ai-decision"
    );


    panel.innerHTML =

    `
    <div class="ai-decision-card">


        <h3>
        🧠 GPT AI Decision
        </h3>


        <p>
        Decision :
        <b>
        ${decision.decision}
        </b>
        </p>


        <p>
        Action :
        <b>
        ${decision.action}
        </b>
        </p>


        <p>
        Confidence :
        <b>
        ${decision.confidence}%
        </b>
        </p>


         <p>
        🎯 Decision Score :
        <br>

        <span
        style="
        font-size:22px;
        font-weight:bold;
        "
        >
        ${decision.decision_score}
        /
        100
        </span>

        </p>



        <p>
        🏆 AI Decision Grade :
        <br>

        <span
        style="
        font-size:22px;
        font-weight:bold;
        "
        >
        ${decision.grade}
        </span>

        </p>


        <p>
        Reason :
        <br>
        ${decision.reason}
        </p>


        <p>
        Summary :
        <br>
        <b>
        ${decision.summary}
        </b>
        </p>


        <hr>


        <h4>
        🧠 AI Decision Intelligence
        </h4>


        <p>
        🏆 Decision Quality :
        <br>

        <b>
        ${result.intelligence.decision_quality}
        </b>

        </p>



        <p>
        🌎 Market Alignment :
        <br>

        <b>
        ${result.intelligence.market_alignment}
        </b>

        </p>



        <p>
        ❤️ Portfolio Health :
        <br>

        <b>
        ${result.intelligence.portfolio_health}
        </b>

        </p>



        <p>
        🏅 Top ETF :
        <br>

        <b>
        ${result.intelligence.top_etf}
        </b>

        </p>



        <p>
        💡 AI Opinion :
        <br>

        ${result.intelligence.ai_opinion}

        </p>


        <p>
        🌎 Market View :
        <br>
        <b>
        ${decision.market_view}
        </b>
        </p>


        <p>
        📌 Recommended Mode :
        <br>
        <b>
        ${decision.recommended_mode.toUpperCase()}
        </b>
        </p>


        <p>
        🛡 Risk Control :
        <br>
        <b>
        ${decision.risk_control}
        </b>
        </p>


        <p>
        🔄 Next Action :
        <br>
        <b>
        ${decision.next_action}
        </b>
        </p>


    </div>
    `;

}



async function loadAIDecisionHistory(){

    const response =
    await fetch(
        "/api/ai-decision/history"
    );


    const result =
    await response.json();


    const panel =
    document.getElementById(
        "ai-decision-history"
    );


    let html = "";


    html +=
    `
    <div class="ai-history-card">

        <h3>
        🕒 AI Decision History
        </h3>
    `;


    result.history.forEach(
        item => {

            html +=
            `
            <div class="ai-history-item">

                <p>
                📌 Decision :
                <b>
                ${item.decision}
                </b>
                </p>


                <p>
                🎯 Score :
                <b>
                ${item.decision_score ?? "-"}
                </b>
                </p>


                <p>
                🏆 Grade :
                <b>
                ${item.grade ?? "-"}
                </b>
                </p>


                <p>
                🌎 Market :
                <b>
                ${item.market_view}
                </b>
                </p>


                <p>
                🏅 Top ETF :
                <b>
                ${item.top_etf}
                </b>
                </p>


                <p>
                🕒 Date :
                <b>
                ${item.created_at}
                </b>
                </p>


            </div>
            `;

        }
    );


    html +=
    `
    </div>
    `;


    panel.innerHTML = html;

}



async function loadAIDecisionSummary(){

    const response =
    await fetch(
        "/api/ai-decision/summary"
    );


    const result =
    await response.json();


    const summary =
    result.summary;


    const panel =
    document.getElementById(
        "ai-decision-summary"
    );


    panel.innerHTML =

    `
    <div class="ai-summary-card">


        <h3>
        📊 AI Decision Analytics
        </h3>


        <p>
        Total Decisions :
        <b>
        ${summary.total_decisions}
        </b>
        </p>


        <p>
        Average Score :
        <b>
        ${summary.average_score}
        / 100
        </b>
        </p>


        <p>
        Latest Decision :
        <b>
        ${summary.latest_decision}
        </b>
        </p>


        <p>
        AI Grade :
        <b>
        ${summary.latest_grade}
        </b>
        </p>


        <p>
        🌎 Market Alignment :
        <b>
        ${summary.market_view}
        </b>
        </p>


        <p>
        🏅 Top ETF :
        <b>
        ${summary.top_etf}
        </b>
        </p>


    </div>
    `;

}



async function loadAIDecisionQuality(){

    const response =
    await fetch(
        "/api/ai-decision/quality"
    );


    const result =
    await response.json();


    const quality =
    result.quality;


    const panel =
    document.getElementById(
        "ai-decision-quality"
    );


    panel.innerHTML =

    `
    <div class="ai-quality-card">

        <h3>
        🧠 AI Decision Quality
        </h3>

        <p>
        Quality Level :
        <b>
        ${quality.quality_level}
        </b>
        </p>

        <p>
        Score Stability :
        <b>
        ${quality.score_stability}
        </b>
        </p>

        <p>
        Recent Trend :
        <b>
        ${quality.recent_trend}
        </b>
        </p>

        <p>
        💡 AI Evaluation :
        <br>
        ${quality.evaluation}
        </p>

    </div>
    `;

}



async function loadAIDecisionTrend(){

    const response =
    await fetch(
        "/api/ai-decision/trend"
    );


    const result =
    await response.json();


    const trend =
    result.trend;


    const panel =
    document.getElementById(
        "ai-decision-trend"
    );


    let trendIcon = "➡";

    if(trend.trend === "Improving"){

        trendIcon = "📈";

    }
    else if(trend.trend === "Declining"){

        trendIcon = "📉";

    }


    panel.innerHTML =

    `
    <div class="ai-trend-card">

        <h3>
        ${trendIcon} AI Decision Trend
        </h3>

        <p>
        Trend :
        <b>
        ${trend.trend}
        </b>
        </p>

        <p>
        Latest Score :
        <b>
        ${trend.latest_score}
        </b>
        </p>

        <p>
        Previous Score :
        <b>
        ${trend.previous_score}
        </b>
        </p>

        <p>
        Score Change :
        <b>
        ${trend.average_change}
        </b>
        </p>

    </div>
    `;

}



async function loadAIDecisionChart(){

    const response =
    await fetch(
        "/api/ai-decision/chart"
    );

    const result =
    await response.json();

    const ctx =
    document
    .getElementById(
        "aiDecisionChart"
    );

    new Chart(ctx,{

        type:"line",

        data:{

            labels:
            result.chart.labels,

            datasets:[{

                label:
                "Decision Score",

                data:
                result.chart.scores,

                borderWidth:3,

                pointRadius:5,

                pointHoverRadius:7,

                tension:0.35,

                fill:false

            }]

        },

        options:{

            responsive:true,

            maintainAspectRatio:false,

            plugins:{

                legend:{
                    display:true
                },

                title:{
                    display:true,
                    text:"AI Decision Score History"
                }

            },

            scales:{

                y:{

                    min:0,

                    max:100,

                    ticks:{

                        stepSize:10

                    }

                }

            }

        }

    });

}



async function loadAIDecisionStatistics(){

    const response =
    await fetch(
        "/api/ai-decision/statistics"
    );


    const result =
    await response.json();


    const statistics =
    result.statistics;


    const panel =
    document.getElementById(
        "ai-decision-statistics"
    );


    panel.innerHTML =

    `
    <div class="ai-statistics-card">


        <h3>
        📊 AI Decision Statistics
        </h3>


        <p>
        Highest Score :
        <b>
        ${statistics.highest_score}
        </b>
        </p>


        <p>
        Lowest Score :
        <b>
        ${statistics.lowest_score}
        </b>
        </p>


        <p>
        Average Score :
        <b>
        ${statistics.average_score}
        </b>
        </p>


        <p>
        Recent Average :
        <b>
        ${statistics.recent_average}
        </b>
        </p>


        <p>
        Score Spread :
        <b>
        ${statistics.score_spread}
        </b>
        </p>


    </div>
    `;

}



async function loadAIDecisionPerformance(){

    const response =
    await fetch(
        "/api/ai-decision/performance"
    );


    const result =
    await response.json();


    const performance =
    result.performance;


    const panel =
    document.getElementById(
        "ai-decision-performance"
    );


    panel.innerHTML =

    `
    <div class="ai-performance-card">


        <h3>
        🧠 AI Decision Performance
        </h3>


        <p>
        Reliability :
        <b>
        ${performance.reliability}
        </b>
        </p>


        <p>
        Total Decisions :
        <b>
        ${performance.total_decisions}
        </b>
        </p>


        <p>
        Average Score :
        <b>
        ${performance.average_score}
        </b>
        </p>


        <p>
        Highest Score :
        <b>
        ${performance.highest_score}
        </b>
        </p>


        <p>
        Lowest Score :
        <b>
        ${performance.lowest_score}
        </b>
        </p>


        <p>
        Latest Score :
        <b>
        ${performance.latest_score}
        </b>
        </p>


    </div>
    `;

}


async function loadAIDecisionReliability(){

    const response =
    await fetch(
        "/api/ai-decision/reliability"
    );


    const result =
    await response.json();


    const reliability =
    result.reliability;


    const panel =
    document.getElementById(
        "ai-decision-reliability"
    );


    panel.innerHTML =

    `
    <div class="ai-reliability-card">


        <h3>
        🛡 AI Decision Reliability
        </h3>


        <p>
        Reliability :
        <b>
        ${reliability.reliability_level}
        </b>
        </p>


        <p>
        Confidence :
        <b>
        ${reliability.confidence}%
        </b>
        </p>


        <p>
        Stability :
        <b>
        ${reliability.stability}
        </b>
        </p>


        <p>
        Average Score :
        <b>
        ${reliability.average_score}
        </b>
        </p>


        <p>
        Score Change :
        <b>
        ${reliability.score_change}
        </b>
        </p>


        <p>
        💡 AI Status :
        <br>
        ${reliability.message}
        </p>


    </div>
    `;

}



async function loadAIAdaptiveStrategy(){

    const response =
    await fetch(
        "/api/ai-decision/adaptive-strategy"
    );


    const result =
    await response.json();


    const strategy =
    result.strategy;


    const panel =
    document.getElementById(
        "ai-adaptive-strategy"
    );


    panel.innerHTML =

    `
    <div class="ai-adaptive-card">


        <h3>
        🤖 AI Adaptive Strategy
        </h3>


        <p>
        Strategy Mode :
        <b>
        ${strategy.strategy_mode}
        </b>
        </p>


        <p>
        Adjustment :
        <b>
        ${strategy.adjustment}
        </b>
        </p>


        <p>
        Confidence :
        <b>
        ${strategy.confidence}
        </b>
        </p>


        <p>
        Risk Control :
        <b>
        ${strategy.risk_control}
        </b>
        </p>


        <p>
        🌎 Market View :
        <b>
        ${strategy.market_view}
        </b>
        </p>


        <p>
        💡 AI Recommendation :
        <br>
        ${strategy.message}
        </p>


    </div>
    `;

}



async function loadAIRebalance(){

    const response =
    await fetch(
        "/api/portfolio/ai-rebalance"
    );


    const result =
    await response.json();


    const recommendation =
    result.recommendation;


    const panel =
    document.getElementById(
        "ai-rebalance"
    );


    let changesHTML = "";


    recommendation.changes.forEach(
        item => {

            changesHTML +=
            `
            <p>
            🏅 ${item.ticker}
            :
            <b>
            ${item.action}
            </b>
            <br>
            ${item.reason}
            </p>
            `;

        }
    );


    panel.innerHTML =

    `
    <div class="ai-rebalance-card">


        <h3>
        🔄 AI Portfolio Rebalance
        </h3>


        <p>
        Rebalance Action :
        <b>
        ${recommendation.rebalance_action}
        </b>
        </p>


        <p>
        Confidence :
        <b>
        ${recommendation.confidence}
        </b>
        </p>


        <p>
        Market View :
        <b>
        ${recommendation.market_view}
        </b>
        </p>


        <p>
        Recommended Mode :
        <b>
        ${recommendation.recommended_mode}
        </b>
        </p>

        

        ${changesHTML}


        <p>
        💡 AI Recommendation :
        <br>
        ${recommendation.message}
        </p>


    </div>
    `;

}



async function loadAIOptimization(){

    const response =
    await fetch(
        "/api/portfolio/ai-optimization"
    );


    const result =
    await response.json();


    const optimization =
    result.optimization;


    const panel =
    document.getElementById(
        "ai-optimization"
    );


    let allocationHTML = "";


    optimization.optimized_allocation.forEach(
        item => {

            allocationHTML +=
            `
            <p>
            🏅 ${item.ticker}
            <br>
            Current :
            <b>
            ${item.current_weight}%
            </b>

            →

            Target :
            <b>
            ${item.target_weight}%
            </b>
            </p>
            `;

        }
    );


    panel.innerHTML =

    `
    <div class="ai-optimization-card">


        <h3>
        🎯 AI Portfolio Optimization
        </h3>


        <p>
        Status :
        <b>
        ${optimization.optimization_status}
        </b>
        </p>


        ${allocationHTML}


        <p>
        💡 AI Message :
        <br>
        ${optimization.message}
        </p>


    </div>
    `;

}
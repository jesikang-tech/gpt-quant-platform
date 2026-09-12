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
        return "🔴";

    return "⚪";
}

function getRankBadge(rank) {

    if(rank === 1)
        return "TOP 1";

    if(rank === 2)
        return "TOP 2";

    if(rank === 3)
        return "TOP 3";

    return "#" + rank;
}

function getSignal(signal) {

    if(signal === "MAINTAIN")
        return "유지";

    if(signal === "BUY")
        return "매수";

    if(signal === "SELL")
        return "매도";

    return signal;
}

function getGradeBadge(grade){

    if(grade === "A")
        return "A";

    if(grade === "B")
        return "B";

    if(grade === "C")
        return "C";

    return grade;
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
        ${getDashboardText("intelligenceTitle")}
        </div>


        <p>
        ${getDashboardText("rankingCount")} :
        <b>
        ${result.count}
        </b>
        </p>


        <p>
        ${getDashboardText("topETF")} :
        <b>
        ${result.data[0].ticker}
        </b>
        </p>


        <p>
        ${getDashboardText("signal")} :
        <b>
        ${getSignal(
        result.data[0].prediction
        )}
        </b>
        </p>


        <div class="intelligence-score">

        ${getDashboardText("aiScore")} :

        <b>
        ${intelligence.score}
        </b>

        </div>


        <p>
        ${getDashboardText("grade")} :
        <b>
        ${intelligence.grade}
        </b>
        </p>


        <div class="recommendation-box">

        <div class="recommendation-title">

        ${getDashboardText("aiRecommendation")}

        </div>


        <div class="recommendation-signal ${
        recommendationData.recommendation.recommendation.toLowerCase()
        }">

        ${recommendationData.recommendation.recommendation}

        </div>


        <div class="recommendation-confidence">

        ${getDashboardText("confidence")}

        <br>

        <b>

        ${recommendationData.recommendation.confidence}

        </b>

        </div>


        <div class="recommendation-reasons">

        <div class="reason-title">

        ${getDashboardText("aiAnalysisReasons")}

        </div>


        <div class="reason-item">

        ${getDashboardText("scoreAnalysis")}

        <br>

        ${recommendationData.recommendation.reasons[0]}

        </div>



        <div class="reason-item">

        ${getDashboardText("rankingAnalysis")}

        <br>

        ${recommendationData.recommendation.reasons[1]}

        </div>



        <div class="reason-item">

        ${getDashboardText("riskAnalysis")}

        <br>

        ${recommendationData.recommendation.reasons[2]}

        </div>


        </div>


        </div>


       <div class="intelligence-opinion">


        ${getDashboardText("gptAnalyst")}

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
            ${getDashboardText("score")}
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
            ${getDashboardText("enhanced")}
            </p>

            <div class="bar">

            <div class="score-fill enhanced"
            style="width:${item.enhanced_score}%">

            </div>

            </div>

            <b>${item.enhanced_score}</b>

            </div>


            <p>
            ${getDashboardText("grade")} :
            ${getGradeBadge(item.grade)}
            </p>


            <p>
            ${getDashboardText("signal")} :
            <span class="signal">
            ${getSignal(item.prediction)}
            </span>
            </p>


            <p>
            ${getDashboardText("returnScore")} :
            <b>
            ${item.return_score}
            </b>
            </p>


            <p>
            ${getDashboardText("trendScore")} :
            <b>
            ${item.trend_score}
            </b>
            </p>


            <p>
            📐 ${getDashboardText("slopeScore")} :
            <b>
            ${item.slope_score}
            </b>
            </p>


            <p>
            ${getDashboardText("finalScore")} :
            <b>
            ${item.final_score}
            </b>
            </p>


            <p>
            ${getDashboardText("stability")} :
            ${item.stability}
            </p>

            <div class="insight">


            <h3>
            ${getDashboardText("gptQuantAiInsight")}
            </h3>


            <p>
            판단 :
            <b>
            ${getSignal(item.prediction)}
            </b>
            </p>


            <p>
            안정성:
            ${item.stability}
            </p>


            <p>
            ${getDashboardText("bonus")} :
            ${item.prediction_bonus}
            </p>


            <p>
            ${getDashboardText("investmentCharacter")} :
            <b>
            ${getDashboardText("stableHolding")}
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

loadAIDecisionOutcomeLearning();

loadAIRebalance();

loadAIOptimization();

loadPortfolioExplainability();


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
    ${getDashboardText("score")} :
    <b>${result.score}</b>
    </p>


    <p>
    ${getDashboardText("enhanced")} :
    <b>${result.enhanced_score}</b>
    </p>


    <h3>
    ${getDashboardText("aiIntelligence")}
    </h3>


    <p>
    ${getDashboardText("returnScore")} :
    <b>${result.return_score}</b>
    </p>


    <p>
    ${getDashboardText("trendScore")} :
    <b>${result.trend_score}</b>
    </p>


    <p>
    📐 ${getDashboardText("slopeScore")} :
    <b>${result.slope_score}</b>
    </p>


    <p>
    ${getDashboardText("finalScore")} :
    <b>${result.final_score}</b>
    </p>


    <p>
    ${getDashboardText("grade")} :
    ${getGradeBadge(result.grade)}
    </p>


    <p>
    ${getDashboardText("signal")} :
    ${getSignal(result.prediction)}
    </p>


    <p>
    ${getDashboardText("stability")} :
    ${result.stability}
    </p>
    
    <hr>

    <p>
    ${getDashboardText("aiInsight")}
    </p>

    <p>
    ${getDashboardText("trend")} :
    ${result.analysis.trend}
    </p>

    <p>
    ${getDashboardText("risk")} :
    ${result.analysis.risk}
    </p>

    <p>
    ${getDashboardText("opinion")} :
    ${result.analysis.opinion}
    </p>

    <p>
    ${getDashboardText("scoreMomentum")} :
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
    ${getDashboardText("strategy")} :
    ${result.strategy}
    </h3>

    `;


    result.portfolio.forEach(item => {


        let cashClass = "";


        if(item.ticker === "CASH"){

            cashClass =
                "portfolio-cash";

        }


        html += `

        <div class="portfolio-card ${cashClass}">


            <div class="ticker">

            ${item.ticker}

            </div>


            <div class="portfolio-weight">

            ${getDashboardText("portfolioWeight")} :
            <b>
            ${item.weight}%
            </b>

            </div>


            <div class="portfolio-score">

            ${getDashboardText("score")} :
            <b>
            ${item.score ?? "-"}
            </b>

            </div>


            <div class="portfolio-optimization">

            ${getDashboardText("aiOptimization")} :
            <b>
            ${item.optimization_score ?? "-"}
            </b>

            </div>


            ${
                item.ticker !== "CASH"
                    ? `

                    <div class="portfolio-factor">

                        <b>
                        ${getDashboardText("factorAnalysis")}
                        </b>

                        <br><br>


                        <div class="factor-item">

                        ${getDashboardText("factorReturn")}

                        <div class="factor-bar">

                            <div
                                class="factor-fill"
                                style="width:${item.return_score ?? 0}%"
                            >
                            </div>

                        </div>

                        <b>
                        ${item.return_score ?? "-"}
                        </b>

                        </div>


                        <div class="factor-item">

                        ${getDashboardText("factorTrend")}

                        <div class="factor-bar">

                            <div
                                class="factor-fill"
                                style="width:${item.trend_score ?? 0}%"
                            >
                            </div>

                        </div>

                        <b>
                        ${item.trend_score ?? "-"}
                        </b>

                        </div>


                        <div class="factor-item">

                        ${getDashboardText("factorSlope")}

                        <div class="factor-bar">

                            <div
                                class="factor-fill"
                                style="width:${item.slope_score ?? 0}%"
                            >
                            </div>

                        </div>

                        <b>
                        ${item.slope_score ?? "-"}
                        </b>

                        </div>


                        <div class="factor-insight">

                        <b>
                        ${getDashboardText("aiFactorInsight")}
                        </b>

                        <br><br>

                        ${getDashboardText("factorReturn")} :
                        <b>
                        ${item.factor_analysis?.return ?? "-"}
                        </b>

                        <br>

                        ${getDashboardText("factorTrend")} :
                        <b>
                        ${item.factor_analysis?.trend ?? "-"}
                        </b>

                        <br>

                        ${getDashboardText("factorSlope")} :
                        <b>
                        ${item.factor_analysis?.slope ?? "-"}
                        </b>

                        </div>

                    </div>






                    </div>

                    `
                    : ""
            }


        </div>

        `;

    });


    let healthColor = "#e74c3c";


    if(
        result.intelligence.health_score >= 90
    ){

        healthColor = "#27ae60";

    }
    else if(
        result.intelligence.health_score >= 80
    ){

        healthColor = "#f39c12";

    }


    let confidenceColor = "#f39c12";


    if(
        result.intelligence.confidence === "HIGH"
    ){

        confidenceColor = "#27ae60";

    }
    else if(
        result.intelligence.confidence === "LOW"
    ){

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
    else if(
        result.intelligence.risk_level === "High Risk"
    ){

        riskColor = "#e74c3c";

    }


    html += `

        <div class="portfolio-intelligence">

            <h3>
            ${getDashboardText("portfolioIntelligence")}
            </h3>


            <p>

            ❤️ ${getDashboardText("healthScore")} :

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

            🛡 ${getDashboardText("riskLevel")} :

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

            🎯 ${getDashboardText("confidence")} :

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

            💰 ${getDashboardText("cashWeight")} :

            ${result.intelligence.cash_weight}%

            </p>


            <p>

            ${getDashboardText("allocation")} :

            ${
                Object.entries(
                    result.intelligence.allocation
                )
                .map(
                    item =>
                        item[0]
                        + " : "
                        + item[1]
                        + "%"
                )
                .join(" / ")
            }

            </p>


            <p>

            ${getDashboardText("marketRegime")} :

            ${result.insight.analytics.market_regime}

            </p>


            <p>

            ${getDashboardText("marketStrength")} :

            ${result.insight.analytics.market_strength}

            </p>


            <p>

            ${getDashboardText("marketConfidence")} :

            ${result.insight.analytics.market_confidence}%

            </p>


            <p>

            ${getDashboardText("aiRebalance")} :

            ${result.intelligence.rebalance}

            </p>

        </div>

    `;


    html += `

        <div class="portfolio-insight">

            <h3>
            ${getDashboardText("portfolioInsight")}
            </h3>


            <p>

            <b>
            ${getDashboardText("summary")}
            </b>

            <br>

            ${result.insight.summary}

            </p>


            <p>

            <b>
            ${getDashboardText("aiOpinion")}
            </b>

            <br>

            ${result.insight.opinion}

            </p>


            <p>

            <b>
            ${getDashboardText("averageScore")}
            </b>

            <br>

            ${result.insight.analytics.average_score}

            </p>


            <p>

            <b>
            ${getDashboardText("topETF")}
            </b>

            <br>

            ${result.insight.analytics.top_etf}

            (
            ${result.insight.analytics.top_score}
            )

            </p>


            <p>

            <b>
            ${getDashboardText("diversification")}
            </b>

            <br>

            ${result.insight.analytics.diversification}

            </p>


            <p>

            💰 Cash Weight

            <br>

            ${result.insight.analytics.cash_weight}%

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
    ${getDashboardText("portfolioHistory")}
    </h3>

    `;


    result.history.forEach(item => {


        html += `

        <div class="history-card">


        <b>
        ${item.mode.toUpperCase()}
        </b>


        <br>


        ${getDashboardText("etf")} :
        ${item.ticker}


        <br>


        ${getDashboardText("portfolioWeight")} :
        ${item.weight}%


        <br>


        ${getDashboardText("score")} :
        ${item.score ?? "-"}


        <br>


        ${getDashboardText("reason")} :
        ${item.reason}


        <br>


        ${getDashboardText("healthScore")} :
        ${item.health_score ?? "-"}


        <br>


        ${getDashboardText("confidence")} :
        ${item.confidence ?? "-"}


        <br>


        ${getDashboardText("marketCondition")} :
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
    ${getDashboardText("portfolioAnalytics")}
    </h3>


    <p>
    ${getDashboardText("totalDecisions")} :
    <b>
    ${analytics.total_history}
    </b>
    </p>


    <p>
    ${getDashboardText("lastSavedAIStrategy")} :
    <br>
    <b>
    ${analytics.latest_mode.toUpperCase()}
    </b>
    </p>


    <p>
    ${getDashboardText("currentViewStrategy")} :
    <br>
    <b>
    ${portfolioMode.toUpperCase()}
    </b>
    </p>


    <h4>
    ${getDashboardText("strategyUsage")}
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
                ${item[1]} ${getDashboardText("times")}
            </div>


        </div>

        `;

    });



    html += `

    <h4>
    ${getDashboardText("averageAllocation")}
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
        ${getDashboardText("marketIntelligence")}
        </h3>


        <p>
        ${getDashboardText("marketCondition")} :
        <b>
        ${market.market}
        </b>
        </p>


        <p>
        ${getDashboardText("averageScore")} :
        <b>
        ${market.average_score}
        </b>
        </p>


        <p>
        ${getDashboardText("confidence")} :
        <b>
        ${market.confidence}
        </b>
        </p>


        <p>
        ${getDashboardText("recommendedStrategy")} :
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
        ${getDashboardText("confidence")} :
        <b>${result.confidence}%</b>
        </p>

        <p>
        ${getDashboardText("averageScore")} :
        <b>${result.avg_score}</b>
        </p>

        <p>
        ${getDashboardText("highestScore")} :
        <b>${result.max_score}</b>
        </p>

        <p>
        ${getDashboardText("lowestScore")} :
        <b>${result.min_score}</b>
        </p>

        <p>
        ${getDashboardText("scoreSpread")} :
        <b>${result.score_spread}</b>
        </p>

        <p>
        ${getDashboardText("marketStrength")} :
        <b>${result.market_strength}</b>
        </p>

        <p>
        ${getDashboardText("breadth")} :
        <b>${result.breadth}</b>
        </p>

        <p>
        ${getDashboardText("risk")} :
        <b>${result.risk}</b>
        </p>

        <p>
        ${getDashboardText("strategy")} :
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
        ${getDashboardText("aiMarketStrategy")}
        </h3>


        <p>
        ${getDashboardText("strategy")} :
        <b>
        ${result.strategy}
        </b>
        </p>


        <p>
        ${getDashboardText("portfolioMode")} :
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
        ${getDashboardText("cashTarget")} :
        <b>
        ${result.cash_target}%
        </b>
        </p>


        <p>
        ${getDashboardText("recommendation")} :
        <b>
        ${result.recommendation}
        </b>
        </p>


        <p>
        ${getDashboardText("marketStrength")} :
        <b>
        ${result.market_strength}
        </b>
        </p>


        <p>
        ${getDashboardText("confidence")} :
        <b>
        ${result.confidence}%
        </b>
        </p>


        <p>
        ${getDashboardText("rebalanceAction")} :
        <b>
        ${result.rebalance_action}
        </b>
        </p>

        <p>
        ${getDashboardText("aiMessage")}
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
        "ai-decision-content"
    );


    panel.innerHTML =

    `
    <div class="ai-decision-card">


        <h3>
        GPT AI Decision
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
        ${getDashboardText("confidence")} :
        <b>
        ${decision.confidence}%
        </b>
        </p>


         <p>
        Decision Score :
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
        ${getDashboardText("aiDecisionGrade")} :
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


    </div>
    `;

}



async function loadDecisionIntelligence() {

    try {

        const response = await fetch(
            "/api/portfolio/decision-intelligence"
        );

        const result = await response.json();

        const panel = document.getElementById(
            "ai-decision-intelligence"
        );

        if (!panel) {

            console.error(
                "AI Decision Intelligence panel not found"
            );

            return;
        }

        if (!result.success || !result.intelligence) {

            panel.innerHTML =
                "AI Decision Intelligence data unavailable.";

            return;
        }

        const intelligence = result.intelligence;
        const intelligenceScore =
            result.intelligence_score || {};

        const decisionConfidence =
            result.decision_confidence || {};

        const decisionConfidenceExplainability =
            result.decision_confidence_explainability || {};

        const decisionConfidenceAssessment =
            result.decision_confidence_assessment || {};

        const decisionConfidenceRecommendation =
            result.decision_confidence_recommendation || {};

        const aiDecisionValidation =
            result.ai_decision_validation || {};

        const aiDecisionValidationExplainability =
            result.ai_decision_validation_explainability || {};

        const validationExplainabilityStatus =
            aiDecisionValidationExplainability.validation_status || "-";

        const validationExplainabilityScore =
            aiDecisionValidationExplainability.validation_score ?? 0;

        const validationExplainabilityDecision =
            aiDecisionValidationExplainability.decision || "-";

        const validationExplainabilityStrategy =
            aiDecisionValidationExplainability.strategy_mode || "-";

        const validationExplainabilityExplanation =
            aiDecisionValidationExplainability.explanation || "-";

        const validationExplainabilityRisk =
            aiDecisionValidationExplainability.risk_explanation || "-";

        const validationExplainabilityConclusion =
            aiDecisionValidationExplainability.conclusion || "-";

        const validationExplainabilityPositiveSignals =
            aiDecisionValidationExplainability.positive_signals || [];

        const validationExplainabilityRiskSignals =
            aiDecisionValidationExplainability.risk_signals || [];

        const validationExplainabilityAttentionSignals =
            aiDecisionValidationExplainability.attention_signals || [];

        const validation =
            aiDecisionValidation.validation || "-";

        const validationScore =
            aiDecisionValidation.validation_score ?? 0;

        const validationDecision =
            aiDecisionValidation.decision || "-";

        const validationStrategy =
            aiDecisionValidation.strategy_mode || "-";

        const validationAlignment =
            aiDecisionValidation.decision_alignment || "-";

        const validationConsistency =
            aiDecisionValidation.decision_consistency || "-";

        const validationConfidence =
            aiDecisionValidation.confidence_score ?? 0;

        const validationReliability =
            aiDecisionValidation.reliability || "-";

        const validationOptimization =
            aiDecisionValidation.optimization_status || "-";

        const validationSummary =
            aiDecisionValidation.summary || "-";

        const validationSignals =
            aiDecisionValidation.validation_signals || [];

        const validationRiskSignals =
            aiDecisionValidation.risk_signals || [];

        const recommendation =
            decisionConfidenceRecommendation.recommendation || "-";

        const recommendationAction =
            decisionConfidenceRecommendation.action || "-";

        const recommendationMonitoring =
            decisionConfidenceRecommendation.monitoring || "-";

        const recommendationScore =
            decisionConfidenceRecommendation.recommendation_score ?? 0;

        const recommendationAssessment =
            decisionConfidenceRecommendation.assessment || "-";

        const recommendationSummary =
            decisionConfidenceRecommendation.summary || "-";

        const assessment =
            decisionConfidenceAssessment.assessment || "-";

        const assessmentScore =
            decisionConfidenceAssessment.confidence_score ?? 0;

        const strongestSignals =
            decisionConfidenceAssessment.strongest_signals || [];

        const assessmentSupportingSignals =
            decisionConfidenceAssessment.supporting_signals || [];

        const attentionSignals =
            decisionConfidenceAssessment.attention_signals || [];

        const assessmentSummary =
            decisionConfidenceAssessment.assessment_summary || "-";

        const positiveSignals =
            decisionConfidenceExplainability.positive_signals || [];

        const supportingSignals =
            decisionConfidenceExplainability.supporting_signals || [];

        const riskSignals =
            decisionConfidenceExplainability.risk_signals || [];

        const confidenceExplanation =
            decisionConfidenceExplainability.explanation || "-";

        const confidenceScore =
            decisionConfidence.confidence_score ?? 0;

        const confidenceLevel =
            decisionConfidence.confidence_level ?? "-";

        const confidenceGrade =
            decisionConfidence.confidence_grade ?? "-";

        const confidenceStatus =
            decisionConfidence.confidence_status ?? "-";

        const confidenceSummary =
            decisionConfidence.confidence_summary ?? "-";

        const score =
            intelligenceScore.intelligence_score ?? 0;

        const grade =
            intelligenceScore.grade ?? "-";

        const level =
            intelligenceScore.intelligence_level ?? "-";

        const components =
            intelligenceScore.components || {};

        const finalDecision =
            result.final_decision || {};

        const finalDecisionGovernance =
            result.final_decision_governance || {};

        const finalDecisionExecutionControl =
            result.final_decision_execution_control || {};

        const finalDecisionExecutionAssurance =
            result.final_decision_execution_assurance || {};

        const finalDecisionExecutionMonitoring =
            result.final_decision_execution_monitoring || {};

        const finalDecisionExecutionFeedback =
            result.final_decision_execution_feedback || {};

        const finalDecisionExecutionReassessment =
            result.final_decision_execution_reassessment || {};

        const finalDecisionLifecycle =
            result.final_decision_lifecycle || {};

        const finalDecisionLifecycleGovernanceControl =
            result.final_decision_lifecycle_governance_control || {};

        const finalDecisionOperationalIntelligence =
            result.final_decision_operational_intelligence || {};

        const finalDecisionIntegratedIntelligence =
            result.final_decision_integrated_intelligence || {};

        const finalDecisionOrchestration =
            result.final_decision_orchestration || {};

        const finalExecutionDecision =
            result.final_execution_decision || {};

        const finalDecisionCertification =
            result.final_decision_certification || {};

        const finalDecisionMasterControl =
            result.final_decision_master_control || {};

        panel.innerHTML = `

            <div class="ai-decision-intelligence-card">

                <h3>
                    ${getDashboardText("aiDecisionIntelligence")}
                </h3>

                <div class="ai-intelligence-score">

                    <div>
                        <span>${getDashboardText("intelligenceScore")}</span>
                        <strong>${score}/100</strong>
                    </div>

                    <div>
                        <span>${getDashboardText("grade")}</span>
                        <strong>${grade}</strong>
                    </div>

                    <div>
                        <span>${getDashboardText("level")}</span>
                        <strong>${level}</strong>
                    </div>

                </div>

                <div class="ai-decision-confidence">

                <h4>
                    ${getDashboardText("decisionConfidenceIntelligence")}
                </h4>

                <div class="ai-intelligence-score">

                    <div>
                        <span>${getDashboardText("confidenceScore")}</span>
                        <strong>${confidenceScore}/100</strong>
                    </div>

                    <div>
                        <span>${getDashboardText("grade")}</span>
                        <strong>${confidenceGrade}</strong>
                    </div>

                    <div>
                        <span>${getDashboardText("level")}</span>
                        <strong>${confidenceLevel}</strong>
                    </div>

                    <div>
                        <span>${getDashboardText("status")}</span>
                        <strong>${confidenceStatus}</strong>
                    </div>

                </div>

                <p>
                    ${getDashboardText("confidenceSummary")}:
                    <br>
                    ${confidenceSummary}
                </p>

            </div>

            <div class="ai-decision-confidence-explainability">

                <h4>
                    ${getDashboardText("confidenceExplainability")}
                </h4>

                <p>
                    ${getDashboardText("positiveSignals")}:
                    <br>
                    ${
                        positiveSignals.length
                            ? positiveSignals
                                .map(
                                    signal =>
                                        `<b>${signal.name}: ${signal.score}</b>`
                                )
                                .join("<br>")
                            : "-"
                    }
                </p>

                <p>
                    ${getDashboardText("supportingSignals")}:
                    <br>
                    ${
                        supportingSignals.length
                            ? supportingSignals
                                .map(
                                    signal =>
                                        `<b>${signal.name}: ${signal.score}</b>`
                                )
                                .join("<br>")
                            : "-"
                    }
                </p>

                <p>
                    ${getDashboardText("riskSignals")}:
                    <br>
                    ${
                        riskSignals.length
                            ? riskSignals
                                .map(
                                    signal =>
                                        `<b>${signal.name}: ${signal.score}</b>`
                                )
                                .join("<br>")
                            : "None"
                    }
                </p>

                <p>
                    ${getDashboardText("explanation")}:
                    <br>
                    ${confidenceExplanation}
                </p>

            </div>

            <div class="ai-decision-confidence-assessment">

            <h4>
                ${getDashboardText("confidenceAssessment")}
            </h4>

            <p>
                ${getDashboardText("assessment")}:
                <br>
                <b>${assessment}</b>
            </p>

            <p>
                ${getDashboardText("confidenceScore")}:
                <br>
                <b>${assessmentScore}/100</b>
            </p>

            <p>
                ${getDashboardText("strongestSignals")}:
                <br>
                ${
                    strongestSignals.length
                        ? strongestSignals
                            .map(
                                signal =>
                                    `<b>${signal.name}: ${signal.score}</b>`
                            )
                            .join("<br>")
                        : "-"
                }
            </p>

            <p>
                ${getDashboardText("supportingSignals")}:
                <br>
                ${
                    assessmentSupportingSignals.length
                        ? assessmentSupportingSignals
                            .map(
                                signal =>
                                    `<b>${signal.name}: ${signal.score}</b>`
                            )
                            .join("<br>")
                        : "-"
                }
            </p>

            <p>
                ${getDashboardText("attentionSignals")}:
                <br>
                ${
                    attentionSignals.length
                        ? attentionSignals
                            .map(
                                signal =>
                                    `<b>${signal.name}: ${signal.score}</b>`
                            )
                            .join("<br>")
                        : "None"
                }
            </p>

            <p>
                ${getDashboardText("assessmentSummary")}:
                <br>
                ${assessmentSummary}
            </p>

        </div>


        <div class="ai-decision-confidence-recommendation">

            <h4>
                ${getDashboardText("decisionConfidenceRecommendation")}
            </h4>

            <p>
                ${getDashboardText("recommendation")}:
                <br>
                <b>${recommendation}</b>
            </p>

            <p>
                ${getDashboardText("action")}:
                <br>
                <b>${recommendationAction}</b>
            </p>

            <p>
                ${getDashboardText("monitoring")}:
                <br>
                <b>${recommendationMonitoring}</b>
            </p>

            <p>
                ${getDashboardText("recommendationScore")}:
                <br>
                <b>${recommendationScore}/100</b>
            </p>

            <p>
                ${getDashboardText("assessment")}:
                <br>
                <b>${recommendationAssessment}</b>
            </p>

            <p>
                ${getDashboardText("recommendationSummary")}:
                <br>
                ${recommendationSummary}
            </p>

        </div>


        <div class="ai-decision-validation">

            <h4>
                ${getDashboardText("aiDecisionValidation")}
            </h4>

            <p>
                ${getDashboardText("validation")}:
                <br>
                <b>${validation}</b>
            </p>

            <p>
                ${getDashboardText("validationScore")}:
                <br>
                <b>${validationScore}/100</b>
            </p>

            <p>
                ${getDashboardText("decision")}:
                <br>
                <b>${validationDecision}</b>
            </p>

            <p>
                ${getDashboardText("strategy")}:
                <br>
                <b>${validationStrategy}</b>
            </p>

            <p>
                ${getDashboardText("decisionAlignment")}:
                <br>
                <b>${validationAlignment}</b>
            </p>

            <p>
                ${getDashboardText("decisionConsistency")}:
                <br>
                <b>${validationConsistency}</b>
            </p>

            <p>
                Confidence:
                <br>
                <b>${validationConfidence}/100</b>
            </p>

            <p>
                ${getDashboardText("reliability")}:
                <br>
                <b>${validationReliability}</b>
            </p>

            <p>
                ${getDashboardText("optimization")}:
                <br>
                <b>${validationOptimization}</b>
            </p>

            <p>
                ${getDashboardText("validationSignals")}:
                <br>
                ${
                    validationSignals.length
                        ? validationSignals
                            .map(
                                signal =>
                                    `<b>${signal.name}: ${signal.status}</b>`
                            )
                            .join("<br>")
                        : "None"
                }
            </p>

            <p>
                ${getDashboardText("riskSignals")}:
                <br>
                ${
                    validationRiskSignals.length
                        ? validationRiskSignals
                            .map(
                                signal =>
                                    `<b>${signal}</b>`
                            )
                            .join("<br>")
                        : "None"
                }
            </p>

            <p>
                ${getDashboardText("validationSummary")}:
                <br>
                ${validationSummary}
            </p>

        </div>



        <div class="ai-decision-validation-explainability">

            <h4>
                ${getDashboardText("aiDecisionValidationExplainability")}
            </h4>

            <p>
                ${getDashboardText("validationStatus")}:
                <br>
                <b>${validationExplainabilityStatus}</b>
            </p>

            <p>
                ${getDashboardText("validationScore")}:
                <br>
                <b>${validationExplainabilityScore}/100</b>
            </p>

            <p>
                ${getDashboardText("decision")}:
                <br>
                <b>${validationExplainabilityDecision}</b>
            </p>

            <p>
                ${getDashboardText("strategy")}:
                <br>
                <b>${validationExplainabilityStrategy}</b>
            </p>

            <p>
                ${getDashboardText("explanation")}:
                <br>
                ${validationExplainabilityExplanation}
            </p>

            <p>
                ${getDashboardText("positiveSignals")}:
                <br>
                ${
                    validationExplainabilityPositiveSignals.length
                        ? validationExplainabilityPositiveSignals
                            .map(
                                signal =>
                                    `<b>${signal.name}: ${signal.value}</b>`
                            )
                            .join("<br>")
                        : "None"
                }
            </p>

            <p>
                ${getDashboardText("riskSignals")}:
                <br>
                ${
                    validationExplainabilityRiskSignals.length
                        ? validationExplainabilityRiskSignals
                            .map(
                                signal =>
                                    `<b>${signal}</b>`
                            )
                            .join("<br>")
                        : "None"
                }
            </p>

            <p>
                ${getDashboardText("attentionSignals")}:
                <br>
                ${
                    validationExplainabilityAttentionSignals.length
                        ? validationExplainabilityAttentionSignals
                            .map(
                                signal =>
                                    `<b>${signal.name}: ${signal.score}</b>`
                            )
                            .join("<br>")
                        : "None"
                }
            </p>

            <p>
                ${getDashboardText("riskExplanation")}:
                <br>
                ${validationExplainabilityRisk}
            </p>

            <p>
                ${getDashboardText("conclusion")}:
                <br>
                ${validationExplainabilityConclusion}
            </p>

        </div>




        <div class="ai-intelligence-components">

            <p>
                ${getDashboardText("decisionScore")}
                <br>
                <b>${components.decision_score ?? 0}</b>
            </p>

            <p>
                ${getDashboardText("decisionQuality")}
                <br>
                <b>${components.decision_quality ?? 0}</b>
            </p>

            <p>
                ${getDashboardText("reliability")}
                <br>
                <b>${components.reliability ?? 0}</b>
            </p>

            <p>
                ${getDashboardText("adaptiveStrategy")}
                <br>
                <b>${components.adaptive_strategy ?? 0}</b>
            </p>

            <p>
                ${getDashboardText("rebalance")}
                <br>
                <b>${components.rebalance ?? 0}</b>
            </p>

            <p>
                ${getDashboardText("optimization")}
                <br>
                <b>${components.optimization ?? 0}</b>
            </p>

        </div>

        <p>
            ${getDashboardText("decision")}:
            <br>
            <b>${intelligence.decision ?? "-"}</b>
        </p>

        <p>
            ${getDashboardText("confidence")}:
            <br>
            <b>${intelligence.confidence ?? "-"}%</b>
        </p>

        <p>
            ${getDashboardText("quality")}:
            <br>
            <b>${intelligence.quality ?? "-"}</b>
        </p>

        <p>
            ${getDashboardText("qualityTrend")}:
            <br>
            <b>${intelligence.quality_trend ?? "-"}</b>
        </p>

        <p>
            ${getDashboardText("reliability")}:
            <br>
            <b>${intelligence.reliability ?? "-"}</b>
        </p>

        <p>
            ${getDashboardText("marketView")}:
            <br>
            <b>${intelligence.market_view ?? "-"}</b>
        </p>

        <p>
            ${getDashboardText("strategyMode")}:
            <br>
            <b>${intelligence.strategy_mode ?? "-"}</b>
        </p>

        <p>
            ${getDashboardText("decisionAlignment")}:
            <br>
            <b>${intelligence.decision_alignment ?? "-"}</b>
        </p>

        <p>
            ${getDashboardText("adaptiveOverride")}:
            <br>
            <b>${intelligence.adaptive_override ? "YES" : "NO"}</b>
        </p>

        <p>
            ${getDashboardText("overrideReason")}:
            <br>
            ${intelligence.adaptive_override_reason || "No adaptive override applied."}
        </p>

        <p>
            ${getDashboardText("finalStrategy")}:
            <br>
            <b>${intelligence.final_strategy ?? "-"}</b>
        </p>

        <p>
            ${getDashboardText("decisionConsistency")}:
            <br>
            <b>${intelligence.decision_consistency ?? "-"}</b>
        </p>

        <p>
            ${getDashboardText("consistencyScore")}:
            <br>
            <b>${intelligence.decision_consistency_score ?? 0}</b>
        </p>

        <p>
            ${getDashboardText("consistencySummary")}:
            <br>
            ${intelligence.decision_consistency_summary ?? "-"}
        </p>

        <p>
            ${getDashboardText("adaptiveAction")}:
            <br>
            <b>${intelligence.adaptive_action ?? "-"}</b>
        </p>

        <p>
            ${getDashboardText("adaptiveConfidence")}:
            <br>
            <b>${intelligence.adaptive_confidence ?? 0}%</b>
        </p>

        <p>
            ${getDashboardText("adaptiveScore")}:
            <br>
            <b>${intelligence.adaptive_score ?? 0}</b>
        </p>

        <p>
            ${getDashboardText("direction")}:
            <br>
            <b>${intelligence.adaptive_direction ?? "-"}</b>
        </p>

        <p>
            ${getDashboardText("momentum")}:
            <br>
            <b>${intelligence.adaptive_momentum ?? "-"}</b>
        </p>

        <p>
            ${getDashboardText("stability")}:
            <br>
            <b>${intelligence.adaptive_stability ?? "-"}</b>
        </p>

        <p>
            ${getDashboardText("gradeStability")}:
            <br>
            <b>${intelligence.adaptive_grade_stability ?? "-"}</b>
        </p>

        <p>
            ${getDashboardText("consistency")}:
            <br>
            <b>${intelligence.adaptive_consistency ?? "-"}</b>
        </p>

        <p>
            ${getDashboardText("adaptiveSummary")}:
            <br>
            ${intelligence.adaptive_summary ?? "-"}
        </p>

        <p>
            ${getDashboardText("rebalanceAction")}:
            <br>
            <b>${intelligence.rebalance_action ?? "-"}</b>
        </p>

        <p>
            ${getDashboardText("optimization")}:
            <br>
            <b>${intelligence.optimization_status ?? "-"}</b>
        </p>

        <p>
           <div class="ai-final-decision-control-chain">

            <h3>
                ${getDashboardText("finalDecisionExecutionControl")}
            </h3>

            <p>
                ${getDashboardText("finalDecision")}:
                <br>
                <b>${finalDecision.decision ?? "-"}</b>
            </p>

            <p>
                ${getDashboardText("action")}:
                <br>
                <b>${finalDecision.action ?? "-"}</b>
            </p>

            <p>
                ${getDashboardText("executionDecision")}:
                <br>
                <b>${finalExecutionDecision.decision ?? "-"}</b>
            </p>

            <p>
                ${getDashboardText("executionStatus")}:
                <br>
                <b>${finalExecutionDecision.execution_status ?? "-"}</b>
            </p>

            <p>
                ${getDashboardText("executionAuthorization")}:
                <br>
                <b>${finalExecutionDecision.execution_authorization ?? "-"}</b>
            </p>

            <p>
                ${getDashboardText("certificationStatus")}:
                <br>
                <b>${finalDecisionCertification.certification_status ?? "-"}</b>
            </p>

            <p>
                ${getDashboardText("certificationScore")}:
                <br>
                <b>${finalDecisionCertification.certification_score ?? 0}/100</b>
            </p>

            <p>
                ${getDashboardText("masterControlStatus")}:
                <br>
                <b>${finalDecisionMasterControl.master_control_status ?? "-"}</b>
            </p>

            <p>
                ${getDashboardText("masterControlAction")}:
                <br>
                <b>${finalDecisionMasterControl.master_control_action ?? "-"}</b>
            </p>

            <p>
                ${getDashboardText("masterControlRisk")}:
                <br>
                <b>${finalDecisionMasterControl.master_control_risk ?? "-"}</b>
            </p>

            <p>
                ${getDashboardText("masterControlScore")}:
                <br>
                <b>${finalDecisionMasterControl.master_control_score ?? 0}/100</b>
            </p>

            <p>
                ${getDashboardText("reassessmentStatus")}:
                <br>
                <b>${finalDecisionExecutionReassessment.reassessment_status ?? "-"}</b>
            </p>

            <p>
                ${getDashboardText("reassessmentRequired")}:
                <br>
                <b>${finalDecisionExecutionReassessment.reassessment_required ? "YES" : "NO"}</b>
            </p>

        </div>

            ${getDashboardText("finalAction")}:
            <br>
            <b>${intelligence.final_action ?? "-"}</b>
        </p>

        <p>
            ${getDashboardText("aiSummary")}:
            <br>
            ${intelligence.summary ?? "-"}
        </p>

    </div>

    `;

}

    catch (error) {

        console.error(
            "AI Decision Intelligence Error",
            error
        );

        const panel = document.getElementById(
            "ai-decision-intelligence"
        );

        if (panel) {

            panel.innerHTML =
                "AI Decision Intelligence loading failed.";

        }

    }

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
        📜 ${getDashboardText("aiDecisionHistory")}
        </h3>
    `;


    result.history.forEach(
        item => {

            html +=
            `
            <div class="ai-history-item">

                <p>
                Decision :
                <b>
                ${item.decision}
                </b>
                </p>


                <p>
                Score :
                <b>
                ${item.decision_score ?? "-"}
                </b>
                </p>


                <p>
                ${getDashboardText("grade")} :
                <b>
                ${item.grade ?? "-"}
                </b>
                </p>


                <p>
                Market :
                <b>
                ${item.market_view}
                </b>
                </p>


                <p>
                Top ETF :
                <b>
                ${item.top_etf}
                </b>
                </p>


                <p>
                📅 Date :
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
        AI Decision Summary
        </h3>


        <p>
        ${getDashboardText("totalDecisions")} :
        <b>
        ${summary.total_decisions}
        </b>
        </p>


        <p>
        ${getDashboardText("averageScore")} :
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
        ${getDashboardText("aiGrade")} :
        <b>
        ${summary.latest_grade}
        </b>
        </p>


        <p>
        Market Alignment :
        <b>
        ${summary.market_view}
        </b>
        </p>


        <p>
        Top ETF :
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
        ${getDashboardText("decisionQuality")}
        </h3>

        <p>
        Quality Level :
        <b>
        ${quality.quality_level}
        </b>
        </p>

        <p>
        ${getDashboardText("stability")} :
        <b>
        ${quality.score_stability}
        </b>
        </p>

        <p>
        ${getDashboardText("qualityTrend")} :
        <b>
        ${quality.recent_trend}
        </b>
        </p>

        <p>
        AI Evaluation :
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


    let trendIcon = "⚪";


    if(
        trend.direction === "UP"
    ){

        trendIcon = "📈";

    }
    else if(
        trend.direction === "DOWN"
    ){

        trendIcon = "📉";

    }


    panel.innerHTML =

    `
    <div class="ai-trend-card">

        <h3>
        ${trendIcon} AI Decision Trend
        </h3>

        <p>
        ${getDashboardText("trend")} :
        <b>
        ${trend.trend}
        </b>
        </p>

        <p>
        ${getDashboardText("latestScore")} :
        <b>
        ${trend.latest_score}
        </b>
        </p>

        <p>
        ${getDashboardText("previousScore")} :
        <b>
        ${trend.previous_score}
        </b>
        </p>

        <p>
        ${getDashboardText("scoreChange")} :
        <b>
        ${trend.score_change}
        </b>
        </p>

        <p>
        Direction :
        <b>
        ${trend.direction}
        </b>
        </p>

        <p>
        ${getDashboardText("stability")} :
        <b>
        ${trend.stability}
        </b>
        </p>

        <p>
        Momentum :
        <b>
        ${trend.momentum}
        </b>
        </p>

        <p>
        ${getDashboardText("gradeStability")} :
        <b>
        ${trend.grade_stability}
        </b>
        </p>

        <p>
        Decision Consistency :
        <b>
        ${trend.consistency}
        </b>
        </p>

        <p>
        Current Decision :
        <b>
        ${trend.decision}
        </b>
        </p>

        <p>
        Summary :
        <br>
        ${trend.summary}
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
        AI Decision Statistics
        </h3>


        <p>
        ${getDashboardText("highestScore")} :
        <b>
        ${statistics.highest_score}
        </b>
        </p>


        <p>
        ${getDashboardText("lowestScore")} :
        <b>
        ${statistics.lowest_score}
        </b>
        </p>


        <p>
        ${getDashboardText("averageScore")} :
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
        ${getDashboardText("scoreSpread")} :
        <b>
        ${statistics.score_spread}
        </b>
        </p>


    </div>
    `;

}



async function loadAIDecisionOutcomeLearning(){

    const response =
    await fetch(
        "/api/ai-decision/outcome-learning-summary"
    );

    const result =
    await response.json();

    const summary =
    result.summary;

    const panel =
    document.getElementById(
        "ai-decision-outcome-learning"
    );

    panel.innerHTML =

    `
    <div class="ai-outcome-learning-card">

        <h3>
        AI Decision Outcome Learning
        </h3>

        <p>
        Total Outcomes :
        <b>
        ${summary.total_outcomes}
        </b>
        </p>

        <p>
        Evaluated Outcomes :
        <b>
        ${summary.evaluated_outcomes}
        </b>
        </p>

        <p>
        Pending Outcomes :
        <b>
        ${summary.pending_outcomes}
        </b>
        </p>

        <p>
        Average Outcome Score :
        <b>
        ${summary.average_outcome_score ?? "-"}
        </b>
        </p>

        <p>
        Average Portfolio Return :
        <b>
        ${summary.average_portfolio_return ?? "-"}
        </b>
        </p>

        <p>
        Positive Outcomes :
        <b>
        ${summary.positive_outcomes}
        </b>
        </p>

        <p>
        Negative Outcomes :
        <b>
        ${summary.negative_outcomes}
        </b>
        </p>

        <p>
        Adaptive Learning Required :
        <b>
        ${summary.adaptive_learning_required}
        </b>
        </p>

        <p>
        Reassessment Required :
        <b>
        ${summary.reassessment_required}
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
        ${getDashboardText("aiDecisionPerformance")}
        </h3>


        <p>
        ${getDashboardText("reliability")} :
        <b>
        ${performance.reliability}
        </b>
        </p>


        <p>
        ${getDashboardText("totalDecisions")} :
        <b>
        ${performance.total_decisions}
        </b>
        </p>


        <p>
        ${getDashboardText("averageScore")} :
        <b>
        ${performance.average_score}
        </b>
        </p>


        <p>
        ${getDashboardText("highestScore")} :
        <b>
        ${performance.highest_score}
        </b>
        </p>


        <p>
        ${getDashboardText("lowestScore")} :
        <b>
        ${performance.lowest_score}
        </b>
        </p>


        <p>
        ${getDashboardText("latestScore")} :
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
        ${getDashboardText("aiDecisionReliability")}
        </h3>


        <p>
        ${getDashboardText("reliability")} :
        <b>
        ${reliability.reliability_level}
        </b>
        </p>


        <p>
        ${getDashboardText("confidence")} :
        <b>
        ${reliability.confidence}%
        </b>
        </p>


        <p>
        ${getDashboardText("stability")} :
        <b>
        ${reliability.stability}
        </b>
        </p>


        <p>
        ${getDashboardText("averageScore")} :
        <b>
        ${reliability.average_score}
        </b>
        </p>


        <p>
        ${getDashboardText("scoreChange")} :
        <b>
        ${reliability.score_change}
        </b>
        </p>


        <p>
        AI Status :
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
        🧠 AI Adaptive Strategy
        </h3>

        <p>
        ${getDashboardText("strategy")} :
        <b>
        ${strategy.strategy}
        </b>
        </p>

        <p>
        Recommended Action :
        <b>
        ${strategy.action}
        </b>
        </p>

        <p>
        ${getDashboardText("confidence")} :
        <b>
        ${strategy.confidence}
        </b>
        </p>

        <p>
        Decision Score :
        <b>
        ${strategy.score}
        </b>
        </p>

        <p>
        Direction :
        <b>
        ${strategy.direction}
        </b>
        </p>

        <p>
        ${getDashboardText("stability")} :
        <b>
        ${strategy.stability}
        </b>
        </p>

        <p>
        Momentum :
        <b>
        ${strategy.momentum}
        </b>
        </p>

        <p>
        ${getDashboardText("gradeStability")} :
        <b>
        ${strategy.grade_stability}
        </b>
        </p>

        <p>
        Decision Consistency :
        <b>
        ${strategy.consistency}
        </b>
        </p>

        <p>
        Summary :
        <br>
        ${strategy.summary}
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
            ${item.ticker}
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
        ${getDashboardText("aiPortfolioRebalance")}
        </h3>


        <p>
        ${getDashboardText("rebalanceAction")} :
        <b>
        ${recommendation.rebalance_action}
        </b>
        </p>


        <p>
        ${getDashboardText("confidence")} :
        <b>
        ${recommendation.confidence}
        </b>
        </p>


        <p>
        ${getDashboardText("marketView")} :
        <b>
        ${recommendation.market_view}
        </b>
        </p>


        <p>
        ${getDashboardText("recommendedMode")} :
        <b>
        ${recommendation.recommended_mode}
        </b>
        </p>

        

        ${changesHTML}


        <p>
        ${getDashboardText("aiRecommendation")} :
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
            ${item.ticker}
            <br>
            ${getDashboardText("current")} :
            <b>
            ${item.current_weight}%
            </b>


            ${getDashboardText("target")} :
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
        ${getDashboardText("aiPortfolioOptimization")}
        </h3>


        <p>
        ${getDashboardText("status")} :
        <b>
        ${optimization.optimization_status}
        </b>
        </p>


        ${allocationHTML}


        <p>
        ${getDashboardText("aiMessage")} :
        <br>
        ${optimization.message}
        </p>


    </div>
    `;

}



async function loadPortfolioExplainability(){

    try{

        const response =
        await fetch(
            "/api/portfolio/explain"
        );


        const result =
        await response.json();


        if(!result.success){

            return;

        }


        const explanation =
        result.explanation;


        const panel =
        document.getElementById(
            "portfolio-explain-content"
        );


        if(!panel){

            return;

        }



        /*
         * AI Decision Summary
         */

        let decisionSummary = "";

        if(
            explanation.decision_summary
        ){

            decisionSummary = `

                <h4>
                AI Decision Summary
                </h4>

                <p>
                ${explanation.decision_summary}
                </p>

            `;

        }



        /*
         * Factor Analysis
         */

        let factorHTML = "";

        if(
            explanation.factor_analysis
        ){

            factorHTML =
            explanation.factor_analysis
            .map(
                factor => `

                    <p>

                    <strong>
                    ${factor.name}
                    </strong>

                    :
                    ${factor.impact}

                    <br>

                    ${factor.reason}

                    </p>

                `
            )
            .join("");

        }



        /*
         * Allocation Reason
         */

        let allocationHTML = "";

        if(
            explanation.allocation_reason
        ){

            allocationHTML =
            explanation.allocation_reason
            .map(
                item => `

                    <p>

                    <strong>
                    ${item.ticker}
                    </strong>

                    ${
                        item.weight !== undefined
                        ? `(${item.weight}%)`
                        : ""
                    }

                    <br>

                    ${item.reason}

                    </p>

                `
            )
            .join("");

        }



        /*
         * Risk Analysis
         */

        let riskHTML = "";

        if(
            explanation.risk_analysis
        ){

            riskHTML = `

                <h4>
                Risk Analysis
                </h4>

                <p>
                <strong>
                Risk Level:
                </strong>
                ${explanation.risk_analysis.risk_level}

                <br>

                <strong>
                Cash Weight:
                </strong>
                ${explanation.risk_analysis.cash_weight}%

                <br>

                ${explanation.risk_analysis.reason}

                </p>

            `;

        }



        /*
         * Market Analysis
         */

        let marketHTML = "";

        if(
            explanation.market_analysis
        ){

            const market =
            explanation.market_analysis;


            marketHTML = `

                <h4>
                Market Analysis
                </h4>

                <p>

                <strong>
                Regime:
                </strong>

                ${market.regime}

                <br>

                <strong>
                Impact:
                </strong>

                ${market.impact}

                <br>

                ${market.reason}

                </p>

            `;

        }



        /*
         * Render Explainability Card
         */

        panel.innerHTML = `

            <h3>
            ${explanation.summary}
            </h3>


            ${decisionSummary}


            <h4>
            Factor Analysis
            </h4>

            ${factorHTML}


            <h4>
            Allocation Reason
            </h4>

            ${allocationHTML}


            ${riskHTML}


            ${marketHTML}

        `;

    }
    catch(error){

        console.error(
            "Portfolio Explainability Error:",
            error
        );

    }

}




async function loadAIDecisionExplainability(){

    try{

        const response =
        await fetch(
            "/api/ai-decision/explain"
        );


        const result =
        await response.json();


        if(!result.success){

            return;

        }


        const explanation =
        result.explanation;


        const panel =
        document.getElementById(
            "ai-decision-explainability-content"
        );


        if(!panel){

            return;

        }


        const market =
        explanation.explanation?.market || {};


        const portfolio =
        explanation.explanation?.portfolio || {};


        const topETF =
        explanation.explanation?.top_etf || {};


        const risk =
        explanation.explanation?.risk || {};


        const confidence =
        explanation.explanation?.confidence || {};


        panel.innerHTML = `

            <h3>
            ${explanation.decision || "UNKNOWN"}
            </h3>


            <p>

            <strong>
            ${getDashboardText("decisionScore")}:
            </strong>

            ${explanation.decision_score ?? 0} / 100

            <br>

            <strong>
            ${getDashboardText("grade")}:
            </strong>

            ${explanation.decision_grade || "-"}

            </p>


            <h4>
            ${getDashboardText("marketContribution")}
            </h4>

            <p>

            <strong>
            ${getDashboardText("confidence")}:
            </strong>

            ${market.confidence ?? 0}%

            <br>

            <strong>
            ${getDashboardText("contribution")}:
            </strong>

            ${market.contribution ?? 0} points

            <br>

            ${market.reason || ""}

            </p>


            <h4>
            ${getDashboardText("portfolioContribution")}
            </h4>

            <p>

            <strong>
            ${getDashboardText("health")}:
            </strong>

            ${portfolio.health_score ?? 0} / 100

            <br>

            <strong>
            ${getDashboardText("risk")}:
            </strong>

            ${portfolio.risk_level || "-"}

            <br>

            <strong>
            ${getDashboardText("contribution")}:
            </strong>

            ${portfolio.contribution ?? 0} points

            <br>

            ${portfolio.reason || ""}

            </p>


            <h4>
            ${getDashboardText("topETFContribution")}
            </h4>

            <p>

            <strong>
            ${getDashboardText("etf")}:
            </strong>

            ${topETF.ticker || "-"}

            <br>

            <strong>
            ${getDashboardText("score")}:
            </strong>

            ${topETF.score ?? 0} / 100

            <br>

            <strong>
            ${getDashboardText("contribution")}:
            </strong>

            ${topETF.contribution ?? 0} points

            <br>

            ${topETF.reason || ""}

            </p>


            <h4>
            ${getDashboardText("riskAssessment")}
            </h4>

            <p>

            <strong>
            ${getDashboardText("riskLevel")}:
            </strong>

            ${risk.risk_level || "-"}

            <br>

            <strong>
            ${getDashboardText("marketRegime")}:
            </strong>

            ${risk.market_regime || "-"}

            <br>

            ${risk.assessment || ""}

            </p>


            <h4>
            ${getDashboardText("decisionConfidence")}
            </h4>

            <p>

            <strong>
            ${getDashboardText("confidence")}:
            </strong>

            ${confidence.confidence ?? 0}%

            <br>

            <strong>
            ${getDashboardText("level")}:
            </strong>

            ${confidence.level || "-"}

            <br>

            ${confidence.reason || ""}

            </p>


            <h4>
            ${getDashboardText("recommendedAction")}
            </h4>

            <p>

            ${explanation.recommended_action || "-"}

            </p>

        `;

    }
    catch(error){

        console.error(
            "AI Decision Explainability Error:",
            error
        );

    }

}




async function askPortfolioAnalyst(){


    const input =
        document.getElementById(
            "portfolio-question"
        );


    const resultBox =
        document.getElementById(
            "portfolio-analyst-result"
        );



    const question =
        input.value.trim();



    if(!question){

        resultBox.innerHTML =
            "질문을 입력해주세요.";

        return;

    }



    resultBox.innerHTML =
        "AI Portfolio Analyst 분석 중...";



    try{


        const response =
            await fetch(
                "/api/portfolio/chat",
                {
                    method:"POST",

                    headers:{
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(
                            {
                                question:
                                    question
                            }
                        )
                }
            );



        const result =
            await response.json();



        const data =
            result.response;



        let html = "";



        html +=
        `
        <h3>
        ${getDashboardText("aiAnswer")}
        </h3>

        <p>
        ${data.answer}
        </p>
        `;



        html +=
        `
        <h3>
        ${getDashboardText("reason")}
        </h3>
        `;



        data.reason.forEach(
            item => {

                html +=
                `
                <p>
                • ${item}
                </p>
                `;

            }
        );



        html +=
        `
        <h3>
        ${getDashboardText("recommendation")}
        </h3>

        <p>
        ${data.recommendation}
        </p>
        `;



        html +=
        `
        <h3>
        ${getDashboardText("confidence")}
        </h3>

        <p>
        ${data.confidence}
        </p>
        `;



        resultBox.innerHTML =
            html;


    }
    catch(error){


        console.error(
            error
        );


        resultBox.innerHTML =
            "AI Analyst 결과 오류";


    }

}





document.addEventListener("DOMContentLoaded", function () {
    loadDecisionIntelligence();
    loadAIDecisionExplainability();
});


/* ETF-Quant-Platform language selector foundation */
let currentDashboardLanguage = "ko";

function toggleLanguageMenu() {
    const menu = document.getElementById("language-menu");

    if (!menu) {
        return;
    }

    menu.hidden = !menu.hidden;
}

function selectDashboardLanguage(language) {
    if (language !== "ko" && language !== "en") {
        return;
    }

    currentDashboardLanguage = language;

    const menu = document.getElementById("language-menu");

    if (menu) {
        menu.hidden = true;
    }

    console.log("DASHBOARD_LANGUAGE:", currentDashboardLanguage);

    applyDashboardLanguage();
}


/* ETF-Quant-Platform minimal dashboard translations */
const DASHBOARD_TRANSLATIONS = {
    ko: {
        dashboardTitle: "GPT Quant ETF 대시보드",
        dashboardSubtitle: "AI 기반 ETF 랭킹 시스템",
        marketRegimeTitle: "AI 시장 국면",
        marketRegimeLoading: "시장 국면 불러오는 중...",
        portfolioOptimizationTitle: "GPT AI 포트폴리오 최적화",
        conservative: "보수형",
        balanced: "균형형",
        aggressive: "공격형",
        languageKorean: "한국어",
        languageEnglish: "English",

        intelligenceTitle: "GPT ETF 인텔리전스",
        aiMarketStrategy: "AI 시장 전략",
        marketStrength: "시장 강도",
        breadth: "시장 폭",
        portfolioMode: "포트폴리오 모드",
        cashTarget: "현금 목표 비중",
        aiInsight: "AI 인사이트",
        trend: "추세",
        risk: "위험",
        opinion: "의견",
        scoreMomentum: "점수 모멘텀",
        aiDecisionGrade: "AI 의사결정 등급",
        aiGrade: "AI 등급",
        aiDecisionIntelligence: "AI 의사결정 인텔리전스",
        intelligenceScore: "인텔리전스 점수",
        grade: "등급",
        level: "수준",
        decisionConfidenceIntelligence: "의사결정 신뢰도 인텔리전스",
        confidenceScore: "신뢰도 점수",
        status: "상태",
        confidenceSummary: "신뢰도 요약",
        confidenceExplainability: "신뢰도 설명가능성",
        positiveSignals: "긍정 신호",
        supportingSignals: "지원 신호",
        riskSignals: "위험 신호",
        explanation: "설명",
        confidenceAssessment: "신뢰도 평가",
        assessment: "평가",
        strongestSignals: "가장 강한 신호",
        attentionSignals: "주의 신호",
        assessmentSummary: "평가 요약",
        decisionConfidenceRecommendation: "의사결정 신뢰도 권고",
        recommendation: "권고",
        action: "조치",
        monitoring: "모니터링",
        recommendationScore: "권고 점수",
        recommendationSummary: "권고 요약",
        aiRecommendation: "AI 추천",
        aiAnalysisReasons: "AI 분석 이유",
        aiMessage: "AI 메시지",
        scoreAnalysis: "점수 분석",
        rankingAnalysis: "랭킹 분석",
        riskAnalysis: "위험 분석",
        aiDecisionHistory: "AI 의사결정 이력",
        aiDecisionValidation: "AI 의사결정 검증",
        validation: "검증",
        validationScore: "검증 점수",
        decision: "의사결정",
        aiPortfolioRebalance: "AI 포트폴리오 리밸런싱",
        aiPortfolioOptimization: "AI 포트폴리오 최적화",
        recommendedMode: "권장 모드",
        enhanced: "향상 점수",
        signal: "시그널",
        returnScore: "수익률 점수",
        trendScore: "트렌드 점수",
        slopeScore: "기울기 점수",
        finalScore: "최종 점수",
        gptQuantAiInsight: "GPT Quant AI 인사이트",
        bonus: "보너스",
        investmentCharacter: "투자 성격",
        stableHolding: "안정적 보유",
        gptAnalyst: "GPT 애널리스트",
        score: "점수",
        confidence: "신뢰도",
        consistency: "일관성",
        strategy: "전략",
        decisionAlignment: "의사결정 정합성",
        decisionConsistency: "의사결정 일관성",
        reliability: "신뢰도",
        optimization: "최적화",
        validationSignals: "검증 신호",
        validationSummary: "검증 요약",
        aiDecisionValidationExplainability: "AI 의사결정 검증 설명가능성",
        validationStatus: "검증 상태",
        riskExplanation: "위험 설명",
        marketContribution: "시장 기여도",
        portfolioContribution: "포트폴리오 기여도",
        health: "건전성",
        topETFContribution: "상위 ETF 기여도",
        etf: "ETF",
        riskAssessment: "위험 평가",
        riskLevel: "위험 수준",
        recommendedAction: "권장 조치",
        contribution: "기여도",
        conclusion: "결론",
        decisionScore: "의사결정 점수",
        decisionQuality: "의사결정 품질",
        adaptiveStrategy: "적응형 전략",
        rebalance: "리밸런싱",
        quality: "품질",
        qualityTrend: "품질 추세",
        marketView: "시장 관점",
        strategyMode: "전략 모드",
        adaptiveOverride: "적응형 오버라이드",
        overrideReason: "오버라이드 이유",
        finalStrategy: "최종 전략",
        consistencyScore: "일관성 점수",
        consistencySummary: "일관성 요약",
        adaptiveAction: "적응형 조치",
        adaptiveConfidence: "적응형 신뢰도",
        adaptiveScore: "적응형 점수",
        direction: "방향",
        momentum: "모멘텀",
        stability: "안정성",
        gradeStability: "등급 안정성",
        adaptiveSummary: "적응형 요약",
        rebalanceAction: "리밸런싱 조치",
        finalDecisionExecutionControl: "최종 의사결정 실행 및 통제",
        finalDecision: "최종 의사결정",
        executionDecision: "실행 의사결정",
        executionStatus: "실행 상태",
        executionAuthorization: "실행 승인",
        certificationStatus: "인증 상태",
        certificationScore: "인증 점수",
        masterControlStatus: "마스터 통제 상태",
        masterControlAction: "마스터 통제 조치",
        masterControlRisk: "마스터 통제 위험",
        masterControlScore: "마스터 통제 점수",
        reassessmentStatus: "재평가 상태",
        reassessmentRequired: "재평가 필요 여부",
        finalAction: "최종 조치",
        aiSummary: "AI 요약",
        rankingCount: "랭킹 종목 수",
        topETF: "상위 ETF",
        aiScore: "AI 점수",
        portfolioWeight: "비중",
        aiOptimization: "AI 최적화",
        factorAnalysis: "팩터 분석",
        factorReturn: "수익률",
        factorTrend: "추세",
        factorSlope: "기울기",
        aiFactorInsight: "AI 팩터 인사이트",
        portfolioIntelligence: "포트폴리오 인텔리전스",
        averageScore: "평균 점수",
        highestScore: "최고 점수",
        lowestScore: "최저 점수",
        scoreSpread: "점수 편차",
        totalDecisions: "전체 의사결정",
        aiDecisionPerformance: "AI 의사결정 성과",
        aiDecisionReliability: "AI 의사결정 신뢰성",
        marketIntelligence: "GPT 시장 인텔리전스",
        marketCondition: "시장 상태",
        latestScore: "최신 점수",
        previousScore: "이전 점수",
        scoreChange: "점수 변화",
        recommendedStrategy: "권장 전략"
    },

    en: {
        dashboardTitle: "GPT Quant ETF Dashboard",
        dashboardSubtitle: "AI Powered ETF Ranking System",
        marketRegimeTitle: "AI Market Regime",
        marketRegimeLoading: "Market Regime Loading...",
        portfolioOptimizationTitle: "GPT AI Portfolio Optimization",
        conservative: "Conservative",
        balanced: "Balanced",
        aggressive: "Aggressive",
        languageKorean: "Korean",
        languageEnglish: "English",

        intelligenceTitle: "GPT ETF Intelligence",
        aiMarketStrategy: "AI Market Strategy",
        marketStrength: "Market Strength",
        breadth: "Breadth",
        portfolioMode: "Portfolio Mode",
        cashTarget: "Cash Target",
        aiInsight: "AI Insight",
        trend: "Trend",
        risk: "Risk",
        opinion: "Opinion",
        scoreMomentum: "Score Momentum",
        aiDecisionGrade: "AI Decision Grade",
        aiGrade: "AI Grade",
        aiDecisionIntelligence: "AI Decision Intelligence",
        intelligenceScore: "Intelligence Score",
        grade: "Grade",
        level: "Level",
        decisionConfidenceIntelligence: "Decision Confidence Intelligence",
        confidenceScore: "Confidence Score",
        status: "Status",
        confidenceSummary: "Confidence Summary",
        confidenceExplainability: "Confidence Explainability",
        positiveSignals: "Positive Signals",
        supportingSignals: "Supporting Signals",
        riskSignals: "Risk Signals",
        explanation: "Explanation",
        confidenceAssessment: "Confidence Assessment",
        assessment: "Assessment",
        strongestSignals: "Strongest Signals",
        attentionSignals: "Attention Signals",
        assessmentSummary: "Assessment Summary",
        decisionConfidenceRecommendation: "Decision Confidence Recommendation",
        recommendation: "Recommendation",
        aiAnswer: "AI Answer",
        reason: "Reason",
        action: "Action",
        monitoring: "Monitoring",
        recommendationScore: "Recommendation Score",
        recommendationSummary: "Recommendation Summary",
        aiRecommendation: "AI Recommendation",
        aiAnalysisReasons: "AI Analysis Reasons",
        aiMessage: "AI Message",
        scoreAnalysis: "Score Analysis",
        rankingAnalysis: "Ranking Analysis",
        riskAnalysis: "Risk Analysis",
        aiDecisionHistory: "AI Decision History",
        aiDecisionValidation: "AI Decision Validation",
        validation: "Validation",
        validationScore: "Validation Score",
        decision: "Decision",
        aiPortfolioRebalance: "AI Portfolio Rebalance",
        aiPortfolioOptimization: "AI Portfolio Optimization",
        recommendedMode: "Recommended Mode",
        enhanced: "Enhanced Score",
        signal: "Signal",
        returnScore: "Return Score",
        trendScore: "Trend Score",
        slopeScore: "Slope Score",
        finalScore: "Final Score",
        gptQuantAiInsight: "GPT Quant AI Insight",
        bonus: "Bonus",
        investmentCharacter: "Investment Character",
        stableHolding: "Stable Holding",
        gptAnalyst: "GPT Analyst",
        score: "Score",
        confidence: "Confidence",
        consistency: "Consistency",
        strategy: "Strategy",
        decisionAlignment: "Decision Alignment",
        decisionConsistency: "Decision Consistency",
        reliability: "Reliability",
        optimization: "Optimization",
        validationSignals: "Validation Signals",
        validationSummary: "Validation Summary",
        aiDecisionValidationExplainability: "AI Decision Validation Explainability",
        validationStatus: "Validation Status",
        riskExplanation: "Risk Explanation",
        marketContribution: "Market Contribution",
        portfolioContribution: "Portfolio Contribution",
        health: "Health",
        topETFContribution: "Top ETF Contribution",
        etf: "ETF",
        riskAssessment: "Risk Assessment",
        riskLevel: "Risk Level",
        recommendedAction: "Recommended Action",
        contribution: "Contribution",
        conclusion: "Conclusion",
        decisionScore: "Decision Score",
        decisionQuality: "Decision Quality",
        adaptiveStrategy: "Adaptive Strategy",
        rebalance: "Rebalance",
        quality: "Quality",
        qualityTrend: "Quality Trend",
        marketView: "Market View",
        strategyMode: "Strategy Mode",
        adaptiveOverride: "Adaptive Override",
        overrideReason: "Override Reason",
        finalStrategy: "Final Strategy",
        consistencyScore: "Consistency Score",
        consistencySummary: "Consistency Summary",
        adaptiveAction: "Adaptive Action",
        adaptiveConfidence: "Adaptive Confidence",
        adaptiveScore: "Adaptive Score",
        direction: "Direction",
        momentum: "Momentum",
        stability: "Stability",
        gradeStability: "Grade Stability",
        adaptiveSummary: "Adaptive Summary",
        rebalanceAction: "Rebalance Action",
        finalDecisionExecutionControl: "Final Decision Execution & Control",
        finalDecision: "Final Decision",
        executionDecision: "Execution Decision",
        executionStatus: "Execution Status",
        executionAuthorization: "Execution Authorization",
        certificationStatus: "Certification Status",
        certificationScore: "Certification Score",
        masterControlStatus: "Master Control Status",
        masterControlAction: "Master Control Action",
        masterControlRisk: "Master Control Risk",
        masterControlScore: "Master Control Score",
        reassessmentStatus: "Reassessment Status",
        reassessmentRequired: "Reassessment Required",
        finalAction: "Final Action",
        aiSummary: "AI Summary",
        rankingCount: "Ranking Count",
        topETF: "Top ETF",
        aiScore: "AI Score",
        portfolioWeight: "Weight",
        aiOptimization: "AI Optimization",
        factorAnalysis: "Factor Analysis",
        factorReturn: "Return",
        factorTrend: "Trend",
        factorSlope: "Slope",
        aiFactorInsight: "AI Factor Insight",
        portfolioIntelligence: "GPT Portfolio Intelligence",
        averageScore: "Average Score",
        highestScore: "Highest Score",
        lowestScore: "Lowest Score",
        scoreSpread: "Score Spread",
        totalDecisions: "Total Decisions",
        aiDecisionPerformance: "AI Decision Performance",
        aiDecisionReliability: "AI Decision Reliability",
        marketIntelligence: "GPT Market Intelligence",
        marketCondition: "Market Condition",
        latestScore: "Latest Score",
        previousScore: "Previous Score",
        scoreChange: "Score Change",
        recommendedStrategy: "Recommended Strategy"
    }
};

function getDashboardText(key) {
    const translations =
        DASHBOARD_TRANSLATIONS[currentDashboardLanguage] ||
        DASHBOARD_TRANSLATIONS.ko;

    return translations[key] || key;
}


function applyDashboardLanguage() {
    const title = document.querySelector("header h1");
    const subtitle = document.querySelector("header p");
    const marketRegimeTitle = document.querySelector("#market-regime h2");
    const marketRegimeContent = document.getElementById("market-regime-content");
    const portfolioTitle = document.querySelector("#portfolio-advisor h2");
    const portfolioModeSelector = document.getElementById(
        "portfolio-mode-selector"
    );

    if (title) {
        title.textContent = getDashboardText("dashboardTitle");
    }

    if (subtitle) {
        subtitle.textContent = getDashboardText("dashboardSubtitle");
    }

    if (marketRegimeTitle) {
        marketRegimeTitle.textContent =
            getDashboardText("marketRegimeTitle");
    }

    if (marketRegimeContent) {
        marketRegimeContent.textContent =
            getDashboardText("marketRegimeLoading");
    }

    if (portfolioTitle) {
        portfolioTitle.textContent =
            getDashboardText("portfolioOptimizationTitle");
    }

    if (portfolioModeSelector) {
        const buttons = portfolioModeSelector.querySelectorAll("button");

        if (buttons.length >= 3) {
            buttons[0].textContent =
                getDashboardText("conservative");

            buttons[1].textContent =
                getDashboardText("balanced");

            buttons[2].textContent =
                getDashboardText("aggressive");
        }
    }
}

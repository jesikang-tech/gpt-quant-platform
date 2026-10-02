let historyChart = null;

let portfolioMode = "balanced";

let portfolioAnalytics = null;


function getRecommendationIcon(signal){

    if(signal === "BUY")
        return "BUY";

    if(signal === "SELL")
        return "SELL";

    if(signal === "MAINTAIN")
        return "HOLD";

    return "N/A";
}

function getConfidenceIcon(confidence){

    if(confidence === "HIGH")
        return "HIGH";

    if(confidence === "MEDIUM")
        return "MEDIUM";

    if(confidence === "LOW")
        return "LOW";

    return "N/A";
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
        return "MAINTAIN";

    if(signal === "BUY")
        return "BUY";

    if(signal === "SELL")
        return "SELL";

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
        ${getDashboardText("rankingTrendGrade")} :
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

        ${recommendationData.recommendation.reasons?.[1] ?? getDashboardText("none")}

        </div>



        <div class="reason-item">

        ${getDashboardText("riskAnalysis")}

        <br>

        ${recommendationData.recommendation.reasons?.[2] ?? getDashboardText("none")}

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
            ${getDashboardText("rankingTrendGrade")} :
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
            ${getDashboardText("slopeScore")} :
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
            ${getDashboardText("rankingStabilityScore")} :
            ${item.stability}
            </p>

            <div class="insight">


            <h3>
            ${getDashboardText("gptQuantAiInsight")}
            </h3>


            <p>
            ${getDashboardText("opinion")} :
            <b>
            ${getSignal(item.prediction)}
            </b>
            </p>


            <p>
            ${getDashboardText("rankingStabilityScore")} :
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



let platformAuthMode = "user";

function setPlatformAuthMode(mode) {
    const passwordInput =
        document.getElementById("platform-auth-password");
    const description =
        document.getElementById("platform-auth-description");
    const message =
        document.getElementById("platform-auth-message");

    platformAuthMode = mode === "admin" ? "admin" : "user";

    if (!passwordInput || !description || !message) {
        return;
    }

    passwordInput.value = "";
    message.textContent = "";

    if (platformAuthMode === "admin") {
        passwordInput.maxLength = 7;
        passwordInput.setAttribute("aria-label", "Admin password");
        description.textContent = "\uAD00\uB9AC\uC790 \uC778\uC99D";
    } else {
        passwordInput.maxLength = 4;
        passwordInput.setAttribute("aria-label", "User password");
        description.textContent = "\uC0AC\uC6A9\uC790 \uC778\uC99D";
    }

    passwordInput.focus();
}

function showPlatformAuthOverlay() {
    const overlay =
        document.getElementById("platform-auth-overlay");

    if (overlay) {
        overlay.hidden = false;
    }
}

function hidePlatformAuthOverlay() {
    const overlay =
        document.getElementById("platform-auth-overlay");

    if (overlay) {
        overlay.hidden = true;
    }
}

function isValidPlatformPassword(password) {
    const requiredLength =
        platformAuthMode === "admin" ? 7 : 4;

    return (
        password.length === requiredLength
        && /^[0-9]+$/.test(password)
    );
}

async function submitPlatformAuthentication(event) {
    event.preventDefault();

    const passwordInput =
        document.getElementById("platform-auth-password");
    const message =
        document.getElementById("platform-auth-message");
    const submitButton =
        document.getElementById("platform-auth-submit");

    if (!passwordInput || !message || !submitButton) {
        return;
    }

    const password = passwordInput.value;

    if (!isValidPlatformPassword(password)) {
        message.textContent =
            platformAuthMode === "admin"
                ? "\uAD00\uB9AC\uC790 \uBE44\uBC00\uBC88\uD638\uB294 7\uC790\uB9AC \uC22B\uC790\uC785\uB2C8\uB2E4."
                : "\uC0AC\uC6A9\uC790 \uBE44\uBC00\uBC88\uD638\uB294 4\uC790\uB9AC \uC22B\uC790\uC785\uB2C8\uB2E4.";
        passwordInput.focus();
        return;
    }

    const endpoint =
        platformAuthMode === "admin"
            ? "/api/auth/admin-login"
            : "/api/auth/login";

    submitButton.disabled = true;
    message.textContent = "";

    try {
        const response = await fetch(
            endpoint,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    password: password
                })
            }
        );

        if (!response.ok) {
            message.textContent =
                "\uBE44\uBC00\uBC88\uD638\uB97C \uD655\uC778\uD574 \uC8FC\uC138\uC694.";
            passwordInput.value = "";
            passwordInput.focus();
            return;
        }

        const result = await response.json();

        if (result.success !== true) {
            message.textContent =
                "\uC778\uC99D\uC5D0 \uC2E4\uD328\uD588\uC2B5\uB2C8\uB2E4.";
            return;
        }

        passwordInput.value = "";

        if (platformAuthMode === "admin") {
            showPlatformAdminPanel();
        } else {
            hidePlatformAuthOverlay();
        }

        setPlatformLogoutButtonVisible(true);
        startDashboard();
    } catch (error) {
        console.error("Platform authentication error:", error);
        message.textContent =
            "\uC778\uC99D \uC11C\uBC84\uC640 \uC5F0\uACB0\uD560 \uC218 \uC5C6\uC2B5\uB2C8\uB2E4.";
    } finally {
        submitButton.disabled = false;
    }
}

function setPlatformLogoutButtonVisible(visible) {
    const logoutButton =
        document.getElementById("platform-logout-button");

    if (logoutButton) {
        logoutButton.hidden = !visible;
    }
}

async function logoutPlatform() {
    const response = await fetch(
        "/api/auth/logout",
        { method: "POST" }
    );

    if (!response.ok) {
        throw new Error("Platform logout failed.");
    }

    hidePlatformAdminPanel();
    setPlatformLogoutButtonVisible(false);

    setPlatformAuthMode("user");
    showPlatformAuthOverlay();
}

async function initializePlatformAuthentication() {
    const form =
        document.getElementById("platform-auth-form");
    const adminToggle =
        document.getElementById("platform-admin-toggle");
    const logoutButton =
        document.getElementById("platform-logout-button");

    if (!form || !adminToggle) {
        console.error("Platform authentication UI is missing.");
        return;
    }

    if (logoutButton) {
        logoutButton.addEventListener(
            "click",
            async function () {
                try {
                    await logoutPlatform();
                } catch (error) {
                    console.error("Platform logout error:", error);
                }
            }
        );
    }

    form.addEventListener(
        "submit",
        submitPlatformAuthentication
    );

    adminToggle.addEventListener(
        "click",
        function () {
            setPlatformAuthMode(
                platformAuthMode === "admin"
                    ? "user"
                    : "admin"
            );
        }
    );

    setPlatformAuthMode("user");
    showPlatformAuthOverlay();

    try {
        const response =
            await fetch("/api/auth/status");

        if (!response.ok) {
            return;
        }

        const status = await response.json();

        if (status.authenticated === true) {
            if (status.role === "admin") {
                showPlatformAdminPanel();
            } else {
                hidePlatformAuthOverlay();
            }

            setPlatformLogoutButtonVisible(true);
            startDashboard();
        }
    } catch (error) {
        console.error(
            "Platform authentication status error:",
            error
        );
    }
}

document.addEventListener(
    "DOMContentLoaded",
    function () {
        initializePlatformAdminPanel();
        initializePlatformAuthentication();
    }
);



function showPlatformAdminPanel() {
    const overlay =
        document.getElementById("platform-auth-overlay");
    const authCard =
        document.querySelector(".platform-auth-card");
    const adminPanel =
        document.getElementById("platform-admin-panel");

    if (!overlay || !authCard || !adminPanel) {
        return;
    }

    authCard.hidden = true;
    adminPanel.hidden = false;
    overlay.hidden = false;
}

function hidePlatformAdminPanel() {
    const authCard =
        document.querySelector(".platform-auth-card");
    const adminPanel =
        document.getElementById("platform-admin-panel");

    if (authCard) {
        authCard.hidden = false;
    }

    if (adminPanel) {
        adminPanel.hidden = true;
    }
}

async function submitUserPasswordChange(event) {
    event.preventDefault();

    const passwordInput =
        document.getElementById("platform-new-user-password");
    const message =
        document.getElementById("platform-admin-message");
    const submitButton =
        document.getElementById("platform-user-password-submit");

    if (!passwordInput || !message || !submitButton) {
        return;
    }

    const password = passwordInput.value;

    if (
        password.length !== 4
        || !/^[0-9]+$/.test(password)
    ) {
        message.textContent =
            "\uC0AC\uC6A9\uC790 \uBE44\uBC00\uBC88\uD638\uB294 4\uC790\uB9AC \uC22B\uC790\uC5EC\uC57C \uD569\uB2C8\uB2E4.";
        passwordInput.focus();
        return;
    }

    submitButton.disabled = true;
    message.textContent = "";

    try {
        const response = await fetch(
            "/api/auth/user-password",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    password: password
                })
            }
        );

        if (!response.ok) {
            message.textContent =
                "\uBE44\uBC00\uBC88\uD638 \uBCC0\uACBD\uC5D0 \uC2E4\uD328\uD588\uC2B5\uB2C8\uB2E4.";
            return;
        }

        const result = await response.json();

        if (result.success !== true) {
            message.textContent =
                "\uBE44\uBC00\uBC88\uD638 \uBCC0\uACBD\uC5D0 \uC2E4\uD328\uD588\uC2B5\uB2C8\uB2E4.";
            return;
        }

        passwordInput.value = "";
        message.textContent =
            "\uC0AC\uC6A9\uC790 \uBE44\uBC00\uBC88\uD638\uAC00 \uBCC0\uACBD\uB418\uC5C8\uC2B5\uB2C8\uB2E4.";
    } catch (error) {
        console.error(
            "User password change error:",
            error
        );
        message.textContent =
            "\uC778\uC99D \uC11C\uBC84\uC640 \uC5F0\uACB0\uD560 \uC218 \uC5C6\uC2B5\uB2C8\uB2E4.";
    } finally {
        submitButton.disabled = false;
    }
}

function initializePlatformAdminPanel() {
    const form =
        document.getElementById("platform-user-password-form");
    const dashboardButton =
        document.getElementById("platform-admin-dashboard");

    if (!form || !dashboardButton) {
        console.error("Platform admin UI is missing.");
        return;
    }

    form.addEventListener(
        "submit",
        submitUserPasswordChange
    );

    dashboardButton.addEventListener(
        "click",
        function () {
            hidePlatformAdminPanel();
            hidePlatformAuthOverlay();
        }
    );
}

let dashboardStarted = false;

function startDashboard() {
    if (dashboardStarted) {
        return;
    }

    dashboardStarted = true;

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
    loadDecisionIntelligence();
    loadAIDecisionExplainability();

    setInterval(loadDashboard, 10000);
    setInterval(loadPortfolioAdvisor, 10000);
    setInterval(loadMarketRegime, 10000);
}


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
    <div class="etf-detail-box">

        <div class="etf-detail-summary">

            <h3>
            ${result.ticker}
            </h3>

            <div class="etf-detail-summary-grid">

                <div class="etf-detail-metric">
                    <span>${getDashboardText("score")}</span>
                    <b>${result.score}</b>
                </div>

                <div class="etf-detail-metric">
                    <span>${getDashboardText("enhanced")}</span>
                    <b>${result.enhanced_score}</b>
                </div>

            </div>

        </div>


        <section class="etf-detail-section">

            <h3>
            ${getDashboardText("aiIntelligence")}
            </h3>

            <div class="etf-detail-data-grid">

                <p>
                    <span>${getDashboardText("returnScore")}</span>
                    <b>${result.return_score}</b>
                </p>

                <p>
                    <span>${getDashboardText("trendScore")}</span>
                    <b>${result.trend_score}</b>
                </p>

                <p>
                    <span>${getDashboardText("slopeScore")}</span>
                    <b>${result.slope_score}</b>
                </p>

                <p>
                    <span>${getDashboardText("finalScore")}</span>
                    <b>${result.final_score}</b>
                </p>

                <p>
                    <span>${getDashboardText("rankingTrendGrade")}</span>
                    <span>${getGradeBadge(result.grade)}</span>
                </p>

                <p>
                    <span>${getDashboardText("signal")}</span>
                    <span>${getSignal(result.prediction)}</span>
                </p>

                <p>
                    <span>${getDashboardText("rankingStabilityScore")}</span>
                    <b>${result.stability}</b>
                </p>

            </div>

        </section>


        <section class="etf-detail-section etf-detail-insight">

            <h3>
            ${getDashboardText("aiInsight")}
            </h3>

            <div class="etf-detail-insight-list">

                <p>
                    <span>${getDashboardText("trend")}</span>
                    <strong>${result.analysis.trend}</strong>
                </p>

                <p>
                    <span>${getDashboardText("risk")}</span>
                    <strong>${result.analysis.risk}</strong>
                </p>

                <p>
                    <span>${getDashboardText("opinion")}</span>
                    <strong>${result.analysis.opinion}</strong>
                </p>

                <p>
                    <span>${getDashboardText("scoreMomentum")}</span>
                    <strong>${Number.isFinite(Number(result.analysis.score_change)) ? Number(result.analysis.score_change).toFixed(1) : result.analysis.score_change}</strong>
                </p>

                <p>
                    <span>Prediction</span>
                    <strong>${result.analysis.prediction}</strong>
                </p>

            </div>

        </section>

    </div>
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

                        ${getDashboardText("returnScore")}

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

                        ${getDashboardText("trendScore")}

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

                        ${getDashboardText("slopeScore")}

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
            ${getDashboardText("healthScore")} :
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
            ${getDashboardText("riskLevel")} :
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

            ${getDashboardText("confidence")} :

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
            ${getDashboardText("cashWeight")} :
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

            &#128225; ${getDashboardText("confidence")} :

            ${result.insight.analytics.market_confidence}%

            </p>


            <p>
            ${getDashboardText("aiPortfolioRebalance")} :
            ${result.intelligence.rebalance}

            </p>

        </div>

    `;


    html += `

        <div class="portfolio-insight">

            <h3>
            ${getDashboardText("gptPortfolioInsight")}
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

            ${getDashboardText("cashWeight")}

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


    const groups = new Map();


    result.history.forEach(item => {

        const key =
        `${item.mode}__${item.created_at}`;


        if (!groups.has(key)) {

            groups.set(
                key,
                {
                    mode: item.mode,
                    created_at: item.created_at,
                    health_score: item.health_score,
                    confidence: item.confidence,
                    market_condition: item.market_condition,
                    items: []
                }
            );

        }


        groups.get(key).items.push(item);

    });


    html += `<div class="history-group-list">`;


    groups.forEach(group => {

        html += `

        <section class="history-group">

            <div class="history-group-header">

                <div>
                    <strong class="history-mode">
                        ${group.mode.toUpperCase()}
                    </strong>

                    <span class="history-group-time">
                        ${group.created_at}
                    </span>
                </div>

                <div class="history-group-summary">

                    <span>
                        ${getDashboardText("healthScore")}
                        <strong>${group.health_score ?? "-"}</strong>
                    </span>

                    <span>
                        ${getDashboardText("confidence")}
                        <strong>${group.confidence ?? "-"}</strong>
                    </span>

                    <span>
                        ${getDashboardText("marketCondition")}
                        <strong>${group.market_condition ?? "-"}</strong>
                    </span>

                </div>

            </div>


            <div class="history-grid">

        `;


        group.items.forEach(item => {

            html += `

            <div class="history-card">

                <div class="history-card-primary">

                    <div class="history-primary-item">
                        <span class="history-label">
                            ${getDashboardText("etf")}
                        </span>
                        <strong>${item.ticker}</strong>
                    </div>

                    <div class="history-primary-item">
                        <span class="history-label">
                            ${getDashboardText("portfolioWeight")}
                        </span>
                        <strong>${item.weight}%</strong>
                    </div>

                    <div class="history-primary-item">
                        <span class="history-label">
                            ${getDashboardText("score")}
                        </span>
                        <strong>${item.score ?? "-"}</strong>
                    </div>

                </div>

                <div class="history-card-details">

                    <div class="history-detail-row">
                        <span>${getDashboardText("reason")}</span>
                        <strong>${item.reason}</strong>
                    </div>

                </div>

            </div>

            `;

        });


        html += `

            </div>

        </section>

        `;

    });


    html += `</div>`;


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


    <div class="portfolio-summary-row">
    <div class="portfolio-summary-item">
        <span class="portfolio-summary-label">
            ${getDashboardText("totalDecisions")}
        </span>
        <b class="portfolio-summary-value">
            ${analytics.total_history}
        </b>
    </div>

    <div class="portfolio-summary-divider"></div>

    <div class="portfolio-summary-item">
        <span class="portfolio-summary-label">
            ${getDashboardText("lastSavedAI")}
        </span>
        <b class="portfolio-summary-value">
            ${analytics.latest_mode.toUpperCase()}
        </b>
    </div>

    <div class="portfolio-summary-divider"></div>

    <div class="portfolio-summary-item">
        <span class="portfolio-summary-label">
            ${getDashboardText("currentViewStrategy")}
        </span>
        <b class="portfolio-summary-value">
            ${portfolioMode.toUpperCase()}
        </b>
    </div>
</div>

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


        <div class="market-info-row">
    <div class="market-info-item">
        <span class="market-info-label">
            ${getDashboardText("marketCondition")}
        </span>
        <b class="market-info-value">
            ${market.market}
        </b>
    </div>

    <div class="market-info-divider"></div>

    <div class="market-info-item">
        <span class="market-info-label">
            ${getDashboardText("averageScore")}
        </span>
        <b class="market-info-value">
            ${market.average_score}
        </b>
    </div>

    <div class="market-info-divider"></div>

    <div class="market-info-item">
        <span class="market-info-label">
            ${getDashboardText("confidence")}
        </span>
        <b class="market-info-value">
            ${market.confidence}
        </b>
    </div>

    <div class="market-info-divider"></div>

    <div class="market-info-item">
        <span class="market-info-label">
            ${getDashboardText("recommendedStrategy")}
        </span>
        <b class="market-info-value">
            ${market.recommended_mode}
        </b>
    </div>
</div>


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
        ${getDashboardText("gptAIDecision")}
        </h3>


        <p>
        ${getDashboardText("decision")} :
        <b>
        ${decision.decision}
        </b>
        </p>


        <p>
        ${getDashboardText("action")} :
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
        ${getDashboardText("decisionScore")} :
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
        ${getDashboardText("reason")} :
        <br>
        ${decision.reason}
        </p>


        <p>
        ${getDashboardText("summary")} :
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
                ${getDashboardText("confidence")}:
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

        <div class="ai-intelligence-components-detail">

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
            ${intelligence.adaptive_override_reason || getDashboardText("noAdaptiveOverride")}
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

        </div>

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

            <p>
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

    </div>

    `;

}

    catch (error) {

        console.error(
            getDashboardText("decisionIntelligenceError"),
            error
        );

        const panel = document.getElementById(
            "ai-decision-intelligence"
        );

        if (panel) {

            panel.innerHTML =
                getDashboardText("decisionIntelligenceLoadingFailed");

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
        ${getDashboardText("aiDecisionHistory")}
        </h3>
    `;


    result.history.forEach(
        item => {

            html +=
            `
            <div class="ai-history-item">

                <p>
                ${getDashboardText("decision")} :
                <b>
                ${item.decision}
                </b>
                </p>


                <p>
                ${getDashboardText("score")} :
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
                ${getDashboardText("market")} :
                <b>
                ${item.market_view}
                </b>
                </p>


                <p>
                ${getDashboardText("topETF")}
                <b>
                ${item.top_etf}
                </b>
                </p>


                <p>
                ${getDashboardText("date")} :
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
        ${getDashboardText("aiDecisionSummary")}
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
        ${getDashboardText("currentDecision")} :
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
        ${getDashboardText("marketView")} :
        <b>
        ${summary.market_view}
        </b>
        </p>


        <p>
        ${getDashboardText("topETF")}
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
        ${getDashboardText("quality")} :
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
        ${getDashboardText("aiEvaluation")} :
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


    let trendIcon = "";


    if(
        trend.direction === "UP"
    ){

        trendIcon = "UP";

    }
    else if(
        trend.direction === "DOWN"
    ){

        trendIcon = "DOWN";

    }


    panel.innerHTML =

    `
    <div class="ai-trend-card">

        <h3>
        ${trendIcon} ${getDashboardText("aiDecisionTrend")}
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
        ${getDashboardText("direction")} :
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
        ${getDashboardText("momentum")} :
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
        ${getDashboardText("decisionConsistency")} :
        <b>
        ${trend.consistency}
        </b>
        </p>

        <p>
        ${getDashboardText("currentDecision")} :
        <b>
        ${trend.decision}
        </b>
        </p>

        <p>
        ${getDashboardText("summary")} :
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
                getDashboardText("decisionScore"),

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
                    text:getDashboardText("aiDecisionScoreHistory")
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
        ${getDashboardText("aiDecisionStatistics")}
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
        ${getDashboardText("recentAverage")} :
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
        ${getDashboardText("aiDecisionOutcomeLearning")}
        </h3>

        <p>
        ${getDashboardText("totalOutcomes")} :
        <b>
        ${summary.total_outcomes}
        </b>
        </p>

        <p>
        ${getDashboardText("evaluatedOutcomes")} :
        <b>
        ${summary.evaluated_outcomes}
        </b>
        </p>

        <p>
        ${getDashboardText("pendingOutcomes")} :
        <b>
        ${summary.pending_outcomes}
        </b>
        </p>

        <p>
        ${getDashboardText("averageOutcomeScore")} :
        <b>
        ${summary.average_outcome_score ?? "-"}
        </b>
        </p>

        <p>
        ${getDashboardText("averagePortfolioReturn")} :
        <b>
        ${summary.average_portfolio_return ?? "-"}
        </b>
        </p>

        <p>
        ${getDashboardText("positiveOutcomes")} :
        <b>
        ${summary.positive_outcomes}
        </b>
        </p>

        <p>
        ${getDashboardText("negativeOutcomes")} :
        <b>
        ${summary.negative_outcomes}
        </b>
        </p>

        <p>
        ${getDashboardText("adaptiveLearningRequired")} :
        <b>
        ${summary.adaptive_learning_required}
        </b>
        </p>

        <p>
        ${getDashboardText("reassessmentRequired")} :
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
        ${getDashboardText("aiStatus")} :
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
        ${getDashboardText("adaptiveStrategy")}
        </h3>

        <p>
        ${getDashboardText("strategy")} :
        <b>
        ${strategy.strategy}
        </b>
        </p>

        <p>
        ${getDashboardText("recommendedAction")} :
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
        ${getDashboardText("decisionScore")} :
        <b>
        ${strategy.score}
        </b>
        </p>

        <p>
        ${getDashboardText("direction")} :
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
        ${getDashboardText("momentum")} :
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
        ${getDashboardText("decisionConsistency")} :
        <b>
        ${strategy.consistency}
        </b>
        </p>

        <p>
        ${getDashboardText("summary")} :
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
                ${getDashboardText("aiDecisionSummary")}
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
                ${getDashboardText("riskAnalysis")}
                </h4>

                <div class="portfolio-explain-grid portfolio-explain-risk-grid">

                    <p>
                    <strong>
                    ${getDashboardText("riskLevel")}
                    </strong>
                    <br>
                    ${explanation.risk_analysis.risk_level}
                    </p>

                    <p>
                    <strong>
                    ${getDashboardText("cashWeight")}
                    </strong>
                    <br>
                    ${explanation.risk_analysis.cash_weight}%
                    </p>

                    <p>
                    <strong>
                    ${getDashboardText("riskAssessment")}
                    </strong>
                    <br>
                    ${explanation.risk_analysis.reason}
                    </p>

                </div>

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
                ${getDashboardText("marketAnalysis")}
                </h4>

                <div class="portfolio-explain-grid portfolio-explain-market-grid">

                    <p>
                    <strong>
                    ${getDashboardText("regime")}
                    </strong>
                    <br>
                    ${market.regime}
                    </p>

                    <p>
                    <strong>
                    ${getDashboardText("impact")}
                    </strong>
                    <br>
                    ${market.impact}
                    </p>

                    <p>
                    <strong>
                    ${getDashboardText("marketReason")}
                    </strong>
                    <br>
                    ${market.reason}
                    </p>

                </div>

            `;

        }



        /*
         * Render Explainability Card
         */

        panel.innerHTML = `

            <div class="portfolio-explain-summary">
                <h3>
                ${explanation.summary}
                </h3>
            </div>


            ${decisionSummary
                ? `<div class="portfolio-explain-section">
                    ${decisionSummary}
                </div>`
                : ""
            }


            <div class="portfolio-explain-section portfolio-explain-factor">

                <h4>
                ${getDashboardText("factorAnalysis")}
                </h4>

                <div class="portfolio-explain-grid">
                    ${factorHTML}
                </div>

            </div>


            <div class="portfolio-explain-section portfolio-explain-allocation">

                <h4>
                ${getDashboardText("allocationReason")}
                </h4>

                <div class="portfolio-explain-grid">
                    ${allocationHTML}
                </div>

            </div>


            ${riskHTML
                ? `<div class="portfolio-explain-section">
                    ${riskHTML}
                </div>`
                : ""
            }


            ${marketHTML
                ? `<div class="portfolio-explain-section">
                    ${marketHTML}
                </div>`
                : ""
            }

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
            <div class="ai-explainability-decision-card">
                <div class="ai-explainability-decision-label">
                    ${getDashboardText("decision")}
                </div>

                <div class="ai-explainability-decision-value">
                    ${explanation.decision || "UNKNOWN"}
                </div>

                <div class="ai-explainability-decision-metrics">
                    <div class="ai-explainability-metric">
                        <span>${getDashboardText("score")}</span>
                        <strong>${explanation.decision_score ?? 0} / 100</strong>
                    </div>

                    <div class="ai-explainability-metric">
                        <span>${getDashboardText("grade")}</span>
                        <strong>${explanation.decision_grade || "-"}</strong>
                    </div>
                </div>
            </div>

            <section class="ai-explainability-section">
                <h3>${getDashboardText("marketContribution")}</h3>

                <div class="ai-explainability-content-grid">
                    <div class="ai-explainability-item">
                        <span>1) ${getDashboardText("confidence")}</span>
                        <strong>${market.confidence ?? 0}%</strong>
                    </div>

                    <div class="ai-explainability-item">
                        <span>2) ${getDashboardText("contribution")}</span>
                        <strong>${market.contribution ?? 0} points</strong>
                    </div>

                    <div class="ai-explainability-item ai-explainability-item-wide">
                        <span>3) ${getDashboardText("reason")}</span>
                        <p>${market.reason || "-"}</p>
                    </div>


                </div>
            </section>

            <section class="ai-explainability-section">
                <h3>${getDashboardText("portfolioContribution")}</h3>

                <div class="ai-explainability-content-grid">
                    <div class="ai-explainability-item">
                        <span>1) ${getDashboardText("health")}</span>
                        <strong>${portfolio.health_score ?? 0} / 100</strong>
                    </div>

                    <div class="ai-explainability-item">
                        <span>2) ${getDashboardText("risk")}</span>
                        <strong>${portfolio.risk_level || "-"}</strong>
                    </div>

                    <div class="ai-explainability-item">
                        <span>3) ${getDashboardText("contribution")}</span>
                        <strong>${portfolio.contribution ?? 0} points</strong>
                    </div>

                    <div class="ai-explainability-item ai-explainability-item-wide">
                        <span>4) ${getDashboardText("reason")}</span>
                        <p>${portfolio.reason || "-"}</p>
                    </div>
                </div>
            </section>

            <section class="ai-explainability-section">
                <h3>${getDashboardText("topETFContribution")}</h3>

                <div class="ai-explainability-content-grid">
                    <div class="ai-explainability-item">
                        <span>1) ${getDashboardText("etf")}</span>
                        <strong>${topETF.ticker || "-"}</strong>
                    </div>

                    <div class="ai-explainability-item">
                        <span>2) ${getDashboardText("score")}</span>
                        <strong>${topETF.score ?? 0} / 100</strong>
                    </div>

                    <div class="ai-explainability-item">
                        <span>3) ${getDashboardText("contribution")}</span>
                        <strong>${topETF.contribution ?? 0} points</strong>
                    </div>

                    <div class="ai-explainability-item ai-explainability-item-wide">
                        <span>4) ${getDashboardText("reason")}</span>
                        <p>${topETF.reason || "-"}</p>
                    </div>
                </div>
            </section>

            <section class="ai-explainability-section">
                <h3>${getDashboardText("riskAssessment")}</h3>

                <div class="ai-explainability-content-grid">
                    <div class="ai-explainability-item">
                        <span>1) ${getDashboardText("riskLevel")}</span>
                        <strong>${risk.risk_level || "-"}</strong>
                    </div>

                    <div class="ai-explainability-item">
                        <span>2) ${getDashboardText("marketRegime")}</span>
                        <strong>${risk.market_regime || "-"}</strong>
                    </div>

                    <div class="ai-explainability-item ai-explainability-item-wide">
                        <span>3) ${getDashboardText("assessment")}</span>
                        <p>${risk.assessment || "-"}</p>
                    </div>
                </div>
            </section>

            <section class="ai-explainability-section">
                <h3>${getDashboardText("decisionConfidence")}</h3>

                <div class="ai-explainability-content-grid">
                    <div class="ai-explainability-item">
                        <span>1) ${getDashboardText("confidence")}</span>
                        <strong>${confidence.confidence ?? 0}%</strong>
                    </div>

                    <div class="ai-explainability-item">
                        <span>2) ${getDashboardText("level")}</span>
                        <strong>${confidence.level || "-"}</strong>
                    </div>

                    <div class="ai-explainability-item ai-explainability-item-wide">
                        <span>3) ${getDashboardText("reason")}</span>
                        <p>${confidence.reason || "-"}</p>
                    </div>

                    <div class="ai-explainability-item ai-explainability-item-wide">
                        <span>4) ${getDashboardText("recommendedAction")}</span>
                        <strong>${explanation.recommended_action || "-"}</strong>
                    </div>                </div>
            </section>

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
            getDashboardText("portfolioQuestionRequired");

        return;

    }



    resultBox.innerHTML =
        getDashboardText("portfolioAnalystAnalyzing");



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
                ${item}
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
            getDashboardText("portfolioAnalystError");


    }

}






let latestHistoricalReplayData = null;

function renderHistoricalReplayResult(data) {
    if (!data) {
        return;
    }

    const statusBox = document.getElementById("historical-replay-status");
    const resultPanel = document.getElementById("historical-replay-result");
    const resultMeta = document.getElementById("historical-replay-result-meta");
    const resultContent = document.getElementById("historical-replay-result-content");

    if (!statusBox || !resultPanel || !resultMeta || !resultContent) {
        return;
    }

    const marketRegime = data.market_regime || {};
    const marketStrategy = data.market_strategy || {};
    const replayPortfolio = Array.isArray(data.portfolio)
        ? data.portfolio
        : [];

    const top10 = Array.isArray(data.current_score_top)
        ? data.current_score_top
        : [];

    resultMeta.textContent =
        `${data.analysis_date} / ${data.period} / ` +
        `${data.lookback_trading_days} ${getDashboardText("historicalReplayTradingDays")} / ` +
        `${getDashboardText("historicalReplayTop")} ${top10.length}`;

    const replayPortfolioRows = replayPortfolio.map((portfolioItem) => {
        const score = portfolioItem.score == null
            ? NaN
            : Number(portfolioItem.score);
        const weight = Number(portfolioItem.weight);

        const scoreText = Number.isFinite(score)
            ? score.toFixed(1)
            : "N/A";

        const weightText = Number.isFinite(weight)
            ? `${weight.toFixed(0)}%`
            : "N/A";

        return `
            <tr>
                <td>${portfolioItem.ticker || ""}</td>
                <td>${weightText}</td>
                <td>${scoreText}</td>
            </tr>
        `;
    }).join("") || `
        <tr>
            <td colspan="3">${getDashboardText("historicalReplayEmptyPortfolio")}</td>
        </tr>
    `;

    const combinedRows = top10.map((item, index) => {
        const price = Number(item.price);
        const finalScore = Number(item.final_score);
        const reality = item.reality_test || {};

        const priceText = Number.isFinite(price)
            ? price.toLocaleString(currentDashboardLanguage === "en" ? "en-US" : "ko-KR")
            : "N/A";

        const scoreText = Number.isFinite(finalScore)
            ? finalScore.toFixed(1)
            : "N/A";

        const closeStatus = reality.close_status ?? "N/A";
        const highStatus = reality.high_status ?? "N/A";

        const closeDay = Number(reality.close_first_hit_day);
        const highDay = Number(reality.high_first_hit_day);
        const observedDays = Number(reality.observed_days);
        const windowDays = Number(reality.window_days);

        const closeDayText = Number.isFinite(closeDay)
            ? `${closeDay}d`
            : "-";

        const highDayText = Number.isFinite(highDay)
            ? `${highDay}d`
            : "-";

        const coverageText =
            Number.isFinite(observedDays) &&
            Number.isFinite(windowDays)
                ? `${observedDays}/${windowDays}`
                : "N/A";

        return `
            <tr>
                <td class="replay-rank">${index + 1}</td>
                <td class="replay-ticker">${item.ticker || ""}</td>
                <td class="replay-name">${item.name || ""}</td>
                <td class="replay-price">${priceText}</td>
                <td class="replay-score">${scoreText}</td>
                <td class="replay-future">${closeStatus}</td>
                <td class="replay-future">${highStatus}</td>
                <td class="replay-observed">${coverageText}</td>
                <td class="replay-hit">${closeDayText}</td>
                <td class="replay-hit">${highDayText}</td>
            </tr>
        `;
    }).join("");

    resultContent.innerHTML = `
        <section class="historical-replay-section historical-replay-portfolio">
            <div class="historical-replay-section-title">
                ${getDashboardText("historicalReplayPortfolioTitle")}
            </div>
            <div class="historical-replay-section-description">
                ${getDashboardText("historicalReplayMarketRegime")}: ${marketRegime.regime || "UNKNOWN"} /
                ${getDashboardText("historicalReplayPortfolioMode")}: ${marketStrategy.portfolio_mode || "balanced"} /
                ${getDashboardText("historicalReplayCashTarget")}: ${marketStrategy.cash_target ?? "N/A"}%
            </div>

            <div class="historical-replay-table-wrap">
                <table class="historical-replay-table historical-replay-portfolio-table">
                    <thead>
                        <tr>
                            <th scope="col">${getDashboardText("historicalReplayTicker")}</th>
                            <th scope="col">${getDashboardText("historicalReplayWeight")}</th>
                            <th scope="col">${getDashboardText("historicalReplayScore")}</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${replayPortfolioRows}
                    </tbody>
                </table>
            </div>
        </section>

        <section class="historical-replay-section historical-replay-combined">
            <div class="historical-replay-section-title">
                ${getDashboardText("historicalReplayRealityTitle")}
            </div>
            <div class="historical-replay-section-description">
                ${getDashboardText("historicalReplayRealityDescription")}
            </div>

            <div class="historical-replay-table-wrap">
                <table class="historical-replay-table historical-replay-combined-table">
                    <thead>
                        <tr>
                            <th scope="col">${getDashboardText("historicalReplayRank")}</th>
                            <th scope="col">${getDashboardText("historicalReplayTicker")}</th>
                            <th scope="col">${getDashboardText("historicalReplayEtfName")}</th>
                            <th scope="col">${getDashboardText("historicalReplayPrice")}</th>
                            <th scope="col">${getDashboardText("historicalReplayScore")}</th>
                            <th scope="col">${getDashboardText("historicalReplayClose")}</th>
                            <th scope="col">${getDashboardText("historicalReplayHigh")}</th>
                            <th scope="col">${getDashboardText("historicalReplayObserved")}</th>
                            <th scope="col">${getDashboardText("historicalReplayCloseHit")}</th>
                            <th scope="col">${getDashboardText("historicalReplayHighHit")}</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${combinedRows}
                    </tbody>
                </table>
            </div>
        </section>
    `;

    resultPanel.hidden = false;
    statusBox.textContent = getDashboardText("historicalReplayComplete");
}

async function runHistoricalReplay() {
    const dateInput = document.getElementById("analysis-date");
    const periodInput = document.getElementById("analysis-period");
    const statusBox = document.getElementById("historical-replay-status");
    const resultPanel = document.getElementById("historical-replay-result");
    const resultMeta = document.getElementById("historical-replay-result-meta");
    const resultContent = document.getElementById("historical-replay-result-content");

    if (!dateInput || !periodInput || !statusBox ||
        !resultPanel || !resultMeta || !resultContent) {
        console.error("Historical Replay controls or result area not found.");
        return;
    }

    const analysisDate = dateInput.value;
    const period = periodInput.value || "3m";

    if (!analysisDate) {
        statusBox.textContent = getDashboardText("historicalReplaySelectDate");
        return;
    }

    statusBox.textContent = getDashboardText("historicalReplayRunning");

    try {
        const response = await fetch(
            `/api/historical-replay?date=${encodeURIComponent(analysisDate)}&period=${encodeURIComponent(period)}`
        );

        const data = await response.json();

        if (!response.ok || !data.success) {
            throw new Error(
                data.message || getDashboardText("historicalReplayExecutionFailed")
            );
        }

        latestHistoricalReplayData = data;

        renderHistoricalReplayResult(data);
    } catch (error) {
        console.error("Historical Replay error:", error);
        resultPanel.hidden = true;
        statusBox.textContent =
            error.message || getDashboardText("historicalReplayExecutionError");
    }
}
document.addEventListener("DOMContentLoaded", function () {
    const replayButton = document.getElementById("historical-replay-button");

    if (replayButton) {
        replayButton.addEventListener("click", runHistoricalReplay);
    }
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
        "dashboardTitle": "GPT Quant ETF Dashboard",
        "dashboardSubtitle": "AI 기반 ETF 순위 시스템",
        "marketRegimeTitle": "AI 시장 국면",
        "marketRegimeLoading": "시장 국면 로딩 중...",
        "portfolioOptimizationTitle": "GPT AI 포트폴리오 최적화",
        "conservative": "보수형",
        "balanced": "균형형",
        "aggressive": "공격형",
        "languageKorean": "한국어",
        "languageEnglish": "영어",
        "intelligenceTitle": "GPT ETF 인텔리전스",
        "aiMarketStrategy": "AI 시장 전략",
        "marketStrength": "시장 강도",
        "breadth": "시장 폭",
        "portfolioMode": "포트폴리오 유형",
        "cashTarget": "목표 현금 비중",
        "aiInsight": "AI 판단",
        "trend": "추세",
        "risk": "위험",
        "opinion": "의견",
        "scoreMomentum": "점수 탄력",
        "aiDecisionGrade": "AI 의사결정 등급",
        "aiGrade": "AI 등급",
        "aiDecisionIntelligence": "AI 의사결정 인텔리전스",
        "intelligenceScore": "인텔리전스 점수",
        "grade": "등급",
        "rankingTrendGrade": "랭킹 추세 등급",
        "rankingStabilityScore": "랭킹 안정성 점수",
        "level": "수준",
        "decisionConfidenceIntelligence": "의사결정 신뢰 지능",
        "confidenceScore": "신뢰도 점수",
        "aiAnalysisReasons": "AI 분석 사유",
        "aiRecommendation": "AI 추천",
        "aiScore": "AI 점수",
        "detailAIInsight": "AI 인사이트",
        "detailAIIntelligence": "AI 인텔리전스",
        "detailEnhanced": "강화 점수 :",
        "detailOpinion": "의견 :",
        "detailPrediction": "예측 :",
        "detailRisk": "위험 :",
        "detailScore": "점수 :",
        "detailScoreMomentum": "점수 탄력 :",
        "detailTrend": "추세 :",
        "etfEnhanced": "강화 점수",
        "etfFinalScore": "최종 점수 :",
        "etfGrade": "등급 :",
        "etfReturnScore": "수익률 점수 :",
        "etfScore": "점수",
        "etfSignal": "신호 :",
        "etfSlopeScore": "기울기 점수 :",
        "etfStability": "안정성 :",
        "etfTrendScore": "추세 점수 :",
        "factorReturn": "수익률 요인",
        "factorSlope": "기울기 요인",
        "factorTrend": "추세 요인",
        "gptPortfolioIntelligence": "GPT 포트폴리오 정보",
        "gptPortfolioInsight": "GPT 포트폴리오 판정",
        "portfolioOptimization": "AI 최적화 :",
        "portfolioStrategy": "포트폴리오 전략 :",
        "portfolioWeight": "포트폴리오 비중",
        "rankingAnalysis": "순위 분석",
        "rankingCount": "순위 개수",
        "scoreAnalysis": "점수 분석",
        "signal": "신호",
        "topETF": "Top ETF",
        "decisionIntelligenceTitle": "의사결정 인텔리전스",
        "aiDecisionHistory": "AI 의사결정 이력",
        "aiDecisionTrend": "AI 의사결정 추세",
        "aiDecisionScoreHistory": "AI 의사결정 점수 이력",
        "recentAverage": "최근 평균",
        "averageOutcomeScore": "평균 결과 점수",
        "status": "상태",
        "confidenceSummary": "신뢰도 요약",
        "confidenceExplainability": "신뢰도 설명화",
        "positiveSignals": "긍정 신호",
        "supportingSignals": "지지 신호",
        "riskSignals": "위험 신호",
        "explanation": "설명",
        "confidenceAssessment": "신뢰도 평가",
        "assessment": "평가",
        "strongestSignals": "최강 신호",
        "attentionSignals": "주의 신호",
        "assessmentSummary": "평가 요약",
        "decisionConfidenceRecommendation": "의사결정 신뢰도 추천",
        "recommendation": "추천",
        "aiAnswer": "AI 답변",
        "reason": "사유",
        "action": "조치",
        "monitoring": "모니터링",
        "recommendationScore": "추천 점수",
        "recommendationSummary": "추천 요약",
        "aiMessage": "AI 메시지",
        "riskAnalysis": "위험 분석",
        "aiDecisionValidation": "AI 의사결정 검증",
        "validation": "검증",
        "validationScore": "검증 점수",
        "decision": "의사결정",
        "aiPortfolioRebalance": "AI 포트폴리오 균형 재조정",
        "aiPortfolioOptimization": "AI 포트폴리오 최적화",
        "recommendedMode": "추천 유형",
        "enhanced": "강화",
        "returnScore": "수익률 점수",
        "trendScore": "추세 점수",
        "slopeScore": "기울기 점수",
        "finalScore": "최종 점수",
        "gptQuantAiInsight": "GPT Quant AI 분별",
        "bonus": "보너스",
        "investmentCharacter": "투자 성격",
        "stableHolding": "안정적 보유",
        "gptAnalyst": "GPT 애널리스트",
        "score": "점수",
        "confidence": "신뢰도",
        "consistency": "일관성",
        "strategy": "전략",
        "decisionAlignment": "의사결정 정렬",
        "decisionConsistency": "의사결정 일관화",
        "reliability": "신뢰성",
        "optimization": "최적화",
        "validationSignals": "검증 신호",
        "validationSummary": "검증 요약",
        "aiDecisionValidationExplainability": "AI 의사결정 검증 설명화",
        "validationStatus": "검증 상태",
        "riskExplanation": "위험성 설명",
        "marketContribution": "시장 기여도",
        "portfolioContribution": "포트폴리오 기여도",
        "health": "건전성",
        "topETFContribution": "Top ETF 기여도",
        "etf": "ETF",
        "riskAssessment": "위험 평가",
        "riskLevel": "위험 수준",
        "recommendedAction": "권장 조치",
        "contribution": "기여도",
        "conclusion": "결론",
        "decisionScore": "의사결정 점수",
        "decisionQuality": "의사결정 품질",
        "adaptiveStrategy": "적응형 전략",
        "rebalance": "재균형",
        "quality": "품질",
        "qualityTrend": "품질 추세",
        "marketView": "시장 관점",
        "strategyMode": "전략 모드",
        "currentDecision": "현재 의사결정",
        "market": "시장",
        "aiPortfolioAnalyst": "AI 포트폴리오 애널리스트",
        "current": "현시점 비중",
        "target": "목표 비중",
        "noAdaptiveOverride": "적응형 의사결정 변경이 적용되지 않음",
        "decisionIntelligenceError": "AI 의사결정 인텔리전스 오류",
        "decisionIntelligenceLoadingFailed": "AI 의사결정 인텔리전스 로딩 실패",
        "gptAIDecision": "GPT AI 의사결정",
        "times": "회",
        "averageAllocation": "평균 배분",
        "gptMarketIntelligence": "GPT 시장 정보",
        "date": "날짜",
        "none": "없음",
        "aiDecisionOutcomeLearning": "AI 의사결정 결과 학습",
        "aiDecisionPerformance": "AI 의사결정 성과",
        "aiDecisionQuality": "AI 의사결정 품질",
        "aiDecisionReliability": "AI 의사결정 신뢰도",
        "aiDecisionStatistics": "AI 의사결정 통계",
        "aiDecisionSummary": "AI 의사결정 요약",
        "allocation": "배분",
        "marketConfidence": "시장 신뢰도",
        "allocationReason": "배분 사유",
        "cashWeight": "현금 비중",
        "decisionConfidence": "의사결정 신뢰도",
        "factorAnalysis": "팩터 분석",
        "healthScore": "건전성 점수",
        "impact": "영향도",
        "marketAnalysis": "시장 분석",
        "marketRegime": "시장 국면",
        "regime": "국면",
        "summary": "요약",
        "aiOpinion": "AI 의견",
        "diversification": "분산 투자",
        "strategyUsage": "전략 활용",
        "adaptiveOverride": "적응형 의사결정 변경",
        "overrideReason": "의사결정 변경 사유",
        "finalStrategy": "최종 전략",
        "consistencyScore": "일관성 점수",
        "consistencySummary": "일관성 요약",
        "adaptiveAction": "적응형 조치",
        "adaptiveConfidence": "적응형 신뢰도",
        "adaptiveScore": "적응형 점수",
        "direction": "방향",
        "momentum": "탄력",
        "stability": "안정성",
        "gradeStability": "등급 안정성",
        "adaptiveSummary": "적응형 요약",
        "rebalanceAction": "재균형 조치",
        "finalDecisionExecutionControl": "최종 의사결정 실행 및 통제",
        "finalDecision": "최종 의사결정",
        "executionDecision": "실행 의사결정",
        "executionStatus": "실행 상태",
        "executionAuthorization": "실행 승인",
        "certificationStatus": "인증 상태",
        "certificationScore": "인증 점수",
        "masterControlStatus": "마스터 통제 상태",
        "masterControlAction": "마스터 통제 조치",
        "masterControlRisk": "마스터 통제 위험",
        "masterControlScore": "마스터 통제 점수",
        "reassessmentStatus": "재평가 상태",
        "reassessmentRequired": "재평가 필요 여부",
        "finalAction": "최종 조치",
        "aiSummary": "AI 요약",
        "aiOptimization": "AI 최적화",
        "aiFactorInsight": "AI 요인 분석",
        "portfolioIntelligence": "GPT 포트폴리오 정보",
        "averageScore": "평균 점수",
        "highestScore": "최고 점수",
        "lowestScore": "최저 점수",
        "scoreSpread": "점수 편차",
        "totalDecisions": "총 의사결정",
        "marketIntelligence": "시장 정보",
        "marketCondition": "시장 상태",
        "latestScore": "최근 점수",
        "previousScore": "이전 점수",
        "scoreChange": "점수 변화",
        "recommendedStrategy": "추천 전략",
        "lastSavedAI": "최근 AI 전략",
        "currentViewStrategy": "현재 시점 전략",
        "aiStatus": "AI 상태",
        "portfolioAnalytics": "포트폴리오 분석",
        "portfolioHistory": "포트폴리오 이력",
        "totalOutcomes": "전체 결과",
        "evaluatedOutcomes": "평가 완료 결과",
        "pendingOutcomes": "평가 대기 결과",
        "averagePortfolioReturn": "평균 포트폴리오 수익률",
        "positiveOutcomes": "긍정 결과",
        "negativeOutcomes": "부정 결과",
        "adaptiveLearningRequired": "적응형 학습 필요 여부",
        "aiEvaluation": "AI 평가",
        "portfolioQuestionRequired": "질문을 입력해주세요.",
        "portfolioAnalystAnalyzing": "AI 포트폴리오 애널리스트 분석 중...",
        "portfolioAnalystError": "AI 포트폴리오 애널리스트 처리 중 오류가 발생했습니다.",
        "aiIntelligence": "AI 정보",
        "marketReason": "시장 판단 사유",
        "historicalReplayTitle": "Historical Replay",
        "historicalReplaySubtitle": "특정 날짜의 시장 상황을 재현하여 당시 Top 10을 확인합니다.",
        "historicalReplayAnalysisDate": "분석일자",
        "historicalReplayAnalysisPeriod": "분석기간",
        "historicalReplayPeriod1m": "1개월 (20 거래일)",
        "historicalReplayPeriod2m": "2개월 (40 거래일)",
        "historicalReplayPeriod3m": "3개월 (60 거래일)",
        "historicalReplayPortfolioTitle": "Historical Replay - 포트폴리오",
        "historicalReplayRealityTitle": "Historical Replay - 최종 점수 및 Reality Test",
        "historicalReplaySelectDate": "분석일자를 선택해주세요.",
        "historicalReplayRunning": "Historical Replay 실행 중...",
        "historicalReplayExecutionFailed": "Historical Replay 실행에 실패했습니다.",
        "historicalReplayEmptyPortfolio": "Replay 포트폴리오가 없습니다.",
        "historicalReplayMarketRegime": "Replay 시장 국면",
        "historicalReplayPortfolioMode": "Replay 포트폴리오 모드",
        "historicalReplayCashTarget": "Replay 현금 목표",
        "historicalReplayTicker": "종목코드",
        "historicalReplayWeight": "비중",
        "historicalReplayScore": "Replay 점수",
        "historicalReplayRank": "순위",
        "historicalReplayEtfName": "ETF 이름",
        "historicalReplayPrice": "가격",
        "historicalReplayClose": "종가",
        "historicalReplayHigh": "고가",
        "historicalReplayObserved": "관측",
        "historicalReplayCloseHit": "종가 Hit",
        "historicalReplayHighHit": "고가 Hit",
        "historicalReplayRealityDescription": "Replay 점수는 분석일 당시 이용 가능한 과거 데이터만으로 계산됩니다. Close, High, Observed 및 Hit 결과는 이후 시장 성과를 보여주며 순위 계산에는 사용되지 않습니다.",
        "historicalReplayComplete": "Historical Replay 완료",
        "historicalReplayExecutionError": "Historical Replay 실행 중 오류가 발생했습니다.",
        "historicalReplayTradingDays": "거래일",
        "historicalReplayTop": "상위"
},
    en: {
        "dashboardTitle": "GPT Quant ETF Dashboard",
        "dashboardSubtitle": "AI Powered ETF Ranking System",
        "marketRegimeTitle": "AI Market Regime",
        "marketRegimeLoading": "Market Regime Loading...",
        "portfolioOptimizationTitle": "GPT AI Portfolio Optimization",
        "conservative": "Conservative",
        "balanced": "Balanced",
        "aggressive": "Aggressive",
        "languageKorean": "Korean",
        "languageEnglish": "English",
        "intelligenceTitle": "GPT ETF Intelligence",
        "aiMarketStrategy": "AI Market Strategy",
        "marketStrength": "Market Strength",
        "breadth": "Market Breadth",
        "portfolioMode": "Portfolio Mode",
        "cashTarget": "Cash Target",
        "aiInsight": "AI Insight",
        "trend": "Trend",
        "risk": "Risk",
        "opinion": "Opinion",
        "scoreMomentum": "Score Momentum",
        "aiDecisionGrade": "AI Decision Grade",
        "aiGrade": "AI Grade",
        "aiDecisionIntelligence": "AI Decision Intelligence",
        "intelligenceScore": "Intelligence Score",
        "grade": "Grade",
        "rankingTrendGrade": "Ranking Trend Grade",
        "rankingStabilityScore": "Ranking Stability Score",
        "level": "Level",
        "decisionConfidenceIntelligence": "Decision Confidence Intelligence",
        "confidenceScore": "Confidence Score",
        "aiAnalysisReasons": "AI Analysis Reasons",
        "aiRecommendation": "AI Recommendation",
        "aiScore": "AI Score",
        "detailAIInsight": "AI Insight",
        "detailAIIntelligence": "AI Intelligence",
        "detailEnhanced": "Enhanced Score :",
        "detailOpinion": "Opinion :",
        "detailPrediction": "Prediction :",
        "detailRisk": "Risk :",
        "detailScore": "Score :",
        "detailScoreMomentum": "Score Momentum :",
        "detailTrend": "Trend :",
        "etfEnhanced": "Enhanced Score",
        "etfFinalScore": "Final Score :",
        "etfGrade": "Grade :",
        "etfReturnScore": "Return Score :",
        "etfScore": "Score",
        "etfSignal": "Signal :",
        "etfSlopeScore": "Slope Score :",
        "etfStability": "Stability :",
        "etfTrendScore": "Trend Score :",
        "factorReturn": "Return",
        "factorSlope": "Slope",
        "factorTrend": "Trend",
        "gptPortfolioIntelligence": "GPT Portfolio Intelligence",
        "gptPortfolioInsight": "GPT Portfolio Insight",
        "portfolioOptimization": "AI Optimization :",
        "portfolioStrategy": "Strategy :",
        "portfolioWeight": "Weight",
        "rankingAnalysis": "Ranking Analysis",
        "rankingCount": "Ranking Count",
        "scoreAnalysis": "Score Analysis",
        "signal": "Signal",
        "topETF": "Top ETF",
        "decisionIntelligenceTitle": "AI Decision Intelligence",
        "aiDecisionHistory": "AI Decision History",
        "aiDecisionScoreHistory": "AI Decision Score History",
        "recentAverage": "Recent Average",
        "averageOutcomeScore": "Average Outcome Score",
        "status": "Status",
        "confidenceSummary": "Confidence Summary",
        "confidenceExplainability": "Confidence Explainability",
        "positiveSignals": "Positive Signals",
        "supportingSignals": "Supporting Signals",
        "riskSignals": "Risk Signals",
        "explanation": "Explanation",
        "confidenceAssessment": "Confidence Assessment",
        "assessment": "Assessment",
        "strongestSignals": "Strongest Signals",
        "attentionSignals": "Attention Signals",
        "assessmentSummary": "Assessment Summary",
        "decisionConfidenceRecommendation": "Decision Confidence Recommendation",
        "recommendation": "Recommendation",
        "aiAnswer": "AI Answer",
        "reason": "Reason",
        "action": "Action",
        "monitoring": "Monitoring",
        "recommendationScore": "Recommendation Score",
        "recommendationSummary": "Recommendation Summary",
        "aiMessage": "AI Message",
        "riskAnalysis": "Risk Analysis",
        "aiDecisionValidation": "AI Decision Validation",
        "validation": "Validation",
        "validationScore": "Validation Score",
        "decision": "Decision",
        "aiPortfolioRebalance": "AI Portfolio Rebalance",
        "aiPortfolioOptimization": "AI Portfolio Optimization",
        "recommendedMode": "Recommended Mode",
        "enhanced": "Enhanced Score",
        "returnScore": "Return Score",
        "trendScore": "Trend Score",
        "slopeScore": "Slope Score",
        "finalScore": "Final Score",
        "gptQuantAiInsight": "GPT Quant AI Insight",
        "bonus": "Bonus",
        "investmentCharacter": "Investment Character",
        "stableHolding": "Stable Holding",
        "gptAnalyst": "GPT Analyst",
        "score": "Score",
        "confidence": "Confidence",
        "consistency": "Consistency",
        "strategy": "Strategy",
        "decisionAlignment": "Decision Alignment",
        "decisionConsistency": "Decision Consistency",
        "reliability": "Reliability",
        "optimization": "Optimization",
        "validationSignals": "Validation Signals",
        "validationSummary": "Validation Summary",
        "aiDecisionValidationExplainability": "AI Decision Validation Explainability",
        "validationStatus": "Validation Status",
        "riskExplanation": "Risk Explanation",
        "marketContribution": "Market Contribution",
        "portfolioContribution": "Portfolio Contribution",
        "health": "Health",
        "topETFContribution": "Top ETF Contribution",
        "etf": "ETF",
        "riskAssessment": "Risk Assessment",
        "riskLevel": "Risk Level",
        "recommendedAction": "Recommended Action",
        "contribution": "Contribution",
        "conclusion": "Conclusion",
        "decisionScore": "Decision Score",
        "decisionQuality": "Decision Quality",
        "adaptiveStrategy": "Adaptive Strategy",
        "rebalance": "Rebalance",
        "quality": "Quality",
        "qualityTrend": "Quality Trend",
        "marketView": "Market View",
        "strategyMode": "Strategy Mode",
        "currentDecision": "Latest Decision",
        "market": "Market",
        "aiPortfolioAnalyst": "AI Portfolio Analyst",
        "current": "Current",
        "target": "Target",
        "noAdaptiveOverride": "No adaptive override applied.",
        "decisionIntelligenceError": "AI Decision Intelligence Error",
        "decisionIntelligenceLoadingFailed": "AI Decision Intelligence loading failed.",
        "gptAIDecision": "GPT AI Decision",
        "times": "times",
        "averageAllocation": "Average Allocation",
        "gptMarketIntelligence": "GPT Market Intelligence",
        "date": "Date",
        "none": "None",
        "aiDecisionOutcomeLearning": "AI Decision Outcome Learning",
        "aiDecisionPerformance": "AI Decision Performance",
        "aiDecisionQuality": "AI Decision Quality",
        "aiDecisionReliability": "AI Decision Reliability",
        "aiDecisionStatistics": "AI Decision Statistics",
        "aiDecisionSummary": "AI Decision Summary",
        "allocation": "Allocation",
        "marketConfidence": "Market Confidence",
        "allocationReason": "Allocation Reason",
        "cashWeight": "Cash Weight",
        "decisionConfidence": "Decision Confidence",
        "factorAnalysis": "Factor Analysis",
        "healthScore": "Health Score",
        "impact": "Impact",
        "marketAnalysis": "Market Analysis",
        "marketRegime": "Market Regime",
        "regime": "Regime",
        "summary": "Summary",
        "aiOpinion": "AI Opinion",
        "diversification": "Diversification",
        "strategyUsage": "Strategy Usage",
        "adaptiveOverride": "Adaptive Override",
        "overrideReason": "Override Reason",
        "finalStrategy": "Final Strategy",
        "consistencyScore": "Consistency Score",
        "consistencySummary": "Consistency Summary",
        "adaptiveAction": "Adaptive Action",
        "adaptiveConfidence": "Adaptive Confidence",
        "adaptiveScore": "Adaptive Score",
        "direction": "Direction",
        "momentum": "Momentum",
        "stability": "Stability",
        "gradeStability": "Grade Stability",
        "adaptiveSummary": "Adaptive Summary",
        "rebalanceAction": "Rebalance Action",
        "finalDecisionExecutionControl": "Final Decision Execution & Control",
        "finalDecision": "Final Decision",
        "executionDecision": "Execution Decision",
        "executionStatus": "Execution Status",
        "executionAuthorization": "Execution Authorization",
        "certificationStatus": "Certification Status",
        "certificationScore": "Certification Score",
        "masterControlStatus": "Master Control Status",
        "masterControlAction": "Master Control Action",
        "masterControlRisk": "Master Control Risk",
        "masterControlScore": "Master Control Score",
        "reassessmentStatus": "Reassessment Status",
        "reassessmentRequired": "Reassessment Required",
        "finalAction": "Final Action",
        "aiSummary": "AI Summary",
        "aiOptimization": "AI Optimization",
        "aiFactorInsight": "AI Factor Insight",
        "portfolioIntelligence": "GPT Portfolio Intelligence",
        "averageScore": "Average Score",
        "highestScore": "Highest Score",
        "lowestScore": "Lowest Score",
        "scoreSpread": "Score Spread",
        "totalDecisions": "Total Decisions",
        "marketIntelligence": "GPT Market Intelligence",
        "marketCondition": "Market Condition",
        "latestScore": "Latest Score",
        "previousScore": "Previous Score",
        "scoreChange": "Score Change",
        "recommendedStrategy": "Recommended Strategy",
        "lastSavedAI": "Last Saved AI Strategy",
        "currentViewStrategy": "Current View Strategy",
        "aiStatus": "AI Status",
        "portfolioAnalytics": "Portfolio Analytics",
        "portfolioHistory": "Portfolio History",
        "adaptiveLearningRequired": "Adaptive Learning Required",
        "aiDecisionTrend": "AI Decision Trend",
        "aiEvaluation": "AI Evaluation",
        "averagePortfolioReturn": "Average Portfolio Return",
        "evaluatedOutcomes": "Evaluated Outcomes",
        "negativeOutcomes": "Negative Outcomes",
        "pendingOutcomes": "Pending Outcomes",
        "positiveOutcomes": "Positive Outcomes",
        "totalOutcomes": "Total Outcomes",
        "portfolioQuestionRequired": "Please enter a question.",
        "portfolioAnalystAnalyzing": "AI Portfolio Analyst analyzing...",
        "portfolioAnalystError": "An error occurred while processing the AI Portfolio Analyst request.",
        "aiIntelligence": "AI Intelligence",
        "marketReason": "Market Reason",
        "historicalReplayTitle": "Historical Replay",
        "historicalReplaySubtitle": "Reproduce market conditions on a specific date and review the Top 10 at that time.",
        "historicalReplayAnalysisDate": "Analysis Date",
        "historicalReplayAnalysisPeriod": "Analysis Period",
        "historicalReplayPeriod1m": "1 Month (20 Trading Days)",
        "historicalReplayPeriod2m": "2 Months (40 Trading Days)",
        "historicalReplayPeriod3m": "3 Months (60 Trading Days)",
        "historicalReplayPortfolioTitle": "Historical Replay - Portfolio",
        "historicalReplayRealityTitle": "Historical Replay - Final Score & Reality Test",
        "historicalReplaySelectDate": "Please select an analysis date.",
        "historicalReplayRunning": "Historical Replay running...",
        "historicalReplayExecutionFailed": "Historical Replay execution failed.",
        "historicalReplayEmptyPortfolio": "No replay portfolio available.",
        "historicalReplayMarketRegime": "Replay Market Regime",
        "historicalReplayPortfolioMode": "Replay Portfolio Mode",
        "historicalReplayCashTarget": "Replay Cash Target",
        "historicalReplayTicker": "Ticker",
        "historicalReplayWeight": "Weight",
        "historicalReplayScore": "Replay Score",
        "historicalReplayRank": "Rank",
        "historicalReplayEtfName": "ETF Name",
        "historicalReplayPrice": "Price",
        "historicalReplayClose": "Close",
        "historicalReplayHigh": "High",
        "historicalReplayObserved": "Observed",
        "historicalReplayCloseHit": "Close Hit",
        "historicalReplayHighHit": "High Hit",
        "historicalReplayRealityDescription": "Replay Score is calculated only from historical data available as of the analysis date. Close, High, Observed and Hit results show subsequent market performance and are not used in the ranking calculation.",
        "historicalReplayComplete": "Historical Replay complete",
        "historicalReplayExecutionError": "Historical Replay execution error.",
        "historicalReplayTradingDays": "trading days",
        "historicalReplayTop": "Top"
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

    const historicalReplayTitle = document.getElementById("historical-replay-title");
    const historicalReplaySubtitle = document.getElementById("historical-replay-subtitle");
    const historicalReplayAnalysisDate = document.getElementById("historical-replay-analysis-date-label");
    const historicalReplayAnalysisPeriod = document.getElementById("historical-replay-analysis-period-label");
    const historicalReplayPeriod1m = document.getElementById("historical-replay-period-1m");
    const historicalReplayPeriod2m = document.getElementById("historical-replay-period-2m");
    const historicalReplayPeriod3m = document.getElementById("historical-replay-period-3m");
    const historicalReplayButton = document.getElementById("historical-replay-button");

    if (historicalReplayTitle) historicalReplayTitle.textContent = getDashboardText("historicalReplayTitle");
    if (historicalReplaySubtitle) historicalReplaySubtitle.textContent = getDashboardText("historicalReplaySubtitle");
    if (historicalReplayAnalysisDate) historicalReplayAnalysisDate.textContent = getDashboardText("historicalReplayAnalysisDate");
    if (historicalReplayAnalysisPeriod) historicalReplayAnalysisPeriod.textContent = getDashboardText("historicalReplayAnalysisPeriod");
    if (historicalReplayPeriod1m) historicalReplayPeriod1m.textContent = getDashboardText("historicalReplayPeriod1m");
    if (historicalReplayPeriod2m) historicalReplayPeriod2m.textContent = getDashboardText("historicalReplayPeriod2m");
    if (historicalReplayPeriod3m) historicalReplayPeriod3m.textContent = getDashboardText("historicalReplayPeriod3m");
    if (historicalReplayButton) historicalReplayButton.textContent = getDashboardText("historicalReplayTitle");

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
    if (latestHistoricalReplayData) {
        renderHistoricalReplayResult(latestHistoricalReplayData);
    }
}

applyDashboardLanguage();

/* ============================================================
   V19: Portfolio reference emojis
   Presentation-only additions. No data or decision logic changed.
   ============================================================ */
/* V20: Portfolio Optimization visual cleanup */

/* FINAL_DECISION_CONTROL_CARD_MARKER */

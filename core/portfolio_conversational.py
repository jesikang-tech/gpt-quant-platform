"""
AI Portfolio Conversational Analyst

Step5-3-67

Purpose:
Analyze user questions about portfolio
and generate explainable AI responses.
"""


class PortfolioConversationalAnalyst:


    def __init__(self):
        pass



    def analyze(
        self,
        question,
        portfolio,
        market_info=None
    ):
        """
        Analyze user question.

        Parameters
        ----------
        question : str
            User portfolio question

        portfolio : list/dict
            Current portfolio

        market_info : dict
            Market regime information


        Returns
        -------
        dict
            AI conversational response
        """


        question_type = self._detect_question_type(
            question
        )


        answer = self._generate_answer(
            question,
            portfolio,
            market_info
        )


        portfolio_context = (
            self._analyze_portfolio_context(
                portfolio
            )
        )


        reasons = self._generate_reasons(
            portfolio,
            market_info,
            question_type
        )


        recommendation = self._generate_action(
            question,
            market_info
        )


        confidence = self._calculate_confidence(
            portfolio,
            market_info
        )


        return {

            "question":
                question,


            "question_type":
                question_type,    


            "answer":
                answer,


            "reason":
                reasons,


            "portfolio_context":
                portfolio_context,    


            "recommendation":
                recommendation,


            "confidence":
                confidence    
            

        }



    def _detect_question_type(
        self,
        question
    ):


        question_lower = (
            question.lower()
        )



        if (
            "위험" in question
            or "리스크" in question
            or "risk" in question_lower
        ):

            return "RISK"



        if (
            "비중" in question
            or "weight" in question_lower
            or "왜" in question
            or "why" in question_lower
        ):

            return "ALLOCATION"



        if (
            "추천" in question
            or "해야" in question
            or "전략" in question
        ):

            return "STRATEGY"



        return "GENERAL"



    def _generate_answer(
        self,
        question,
        portfolio,
        market_info
    ):


        question_lower = (
            question.lower()
        )


        if (
            "위험" in question
            or "risk" in question_lower
        ):

            return (
                "현재 포트폴리오는 분산 투자와 "
                "현금 비중을 통해 위험을 관리하고 있습니다."
            )


        if (
            "비중" in question
            or "weight" in question_lower
        ):

            top_asset = max(
                portfolio,
                key=lambda x:
                x.get("score") or 0
            )


            return (

                f"{top_asset['ticker']}은 "
                f"현재 포트폴리오에서 "
                f"가장 높은 Score "
                f"{top_asset['score']}점을 가진 "
                f"핵심 ETF입니다. "

                f"AI는 Factor Intelligence와 "
                f"포트폴리오 최적화를 기반으로 "
                f"{top_asset['weight']}% 비중을 "
                f"배정했습니다."

            )

        

        if (
            "왜" in question
            or "why" in question_lower
        ):

            return (
                "AI는 수익성, 추세 강도, 위험 균형을 "
                "종합 분석하여 현재 포트폴리오를 선택했습니다."
            )


        return (
            "현재 포트폴리오는 시장 상황과 "
            "ETF Intelligence Score를 기반으로 "
            "분석되었습니다."
        )




    def _generate_reasons(
        self,
        portfolio,
        market_info=None,
        question_type=None
    ):


        reasons = []


        if question_type == "RISK":

            return self._generate_risk_reasons(
                portfolio,
                market_info
            )


        if not portfolio:

            return reasons



        top_asset = max(
            portfolio,
            key=lambda x:
            x.get("score") or 0
        )



        ticker = top_asset.get(
            "ticker",
            ""
        )


        score = top_asset.get(
            "score",
            0
        )


        weight = top_asset.get(
            "weight",
            0
        )



        reasons.append(

            f"{ticker} achieved "
            f"highest factor score "
            f"({score})"

        )



        reasons.append(

            f"{ticker} allocated "
            f"{weight}% as core holding"

        )



        cash_asset = next(

            (
                item
                for item in portfolio
                if item.get(
                    "ticker"
                )
                == "CASH"

            ),

            None

        )



        if cash_asset:


            cash_weight = cash_asset.get(
                "weight",
                0
            )


            reasons.append(

                f"Portfolio maintains "
                f"{cash_weight}% cash buffer "
                "for risk control"

            )



        if market_info:


            regime = market_info.get(
                "regime"
            )


            if regime:


                reasons.append(

                    f"Current market regime "
                    f"is {regime}"

                )



        return reasons




    def _generate_risk_reasons(
        self,
        portfolio,
        market_info=None
    ):


        reasons = []


        if not portfolio:

            return reasons



        cash_asset = next(

            (
                item
                for item in portfolio
                if item.get(
                    "ticker"
                ) == "CASH"

            ),

            None

        )


        if cash_asset:

            cash_weight = cash_asset.get(
                "weight",
                0
            )

            reasons.append(

                f"Portfolio maintains "
                f"{cash_weight}% cash buffer "
                "for risk control"

            )


        if len(portfolio) >= 3:

            reasons.append(

                "Portfolio diversification "
                "reduces concentration risk"

            )


        reasons.append(

            "Portfolio allocation balances "
            "return potential and risk exposure"

        )


        if market_info:

            regime = market_info.get(
                "regime"
            )

            if regime:

                reasons.append(

                    f"Current market regime "
                    f"is {regime}"

                )


        return reasons




    def _generate_action(
        self,
        question,
        market_info
    ):


        if not market_info:

            return (
                "Maintain current allocation "
                "and monitor market changes."
            )


        regime = market_info.get(
            "regime",
            "UNKNOWN"
        )


        if regime == "BULL":

            return (
                "Market condition is BULL. "
                "Maintain growth exposure while "
                "monitoring momentum strength."
            )


        elif regime == "BEAR":

            return (
                "Market condition is BEAR. "
                "Consider reducing aggressive exposure "
                "and increasing risk control."
            )


        elif regime == "NEUTRAL":

            return (
                "Market condition is NEUTRAL with "
                "stable factor signals. "
                "Current allocation can be maintained "
                "while monitoring volatility changes."
            )


        return (
            f"Market condition is {regime}. "
            "Monitor market changes and adjust strategy "
            "if necessary."
        )




    def _calculate_confidence(
        self,
        portfolio,
        market_info=None
    ):


        if not portfolio:

            return "LOW"



        top_score = max(

            item.get("score") or 0

            for item in portfolio

        )



        confidence = "MEDIUM"



        if top_score >= 90:

            confidence = "HIGH"



        elif top_score < 70:

            confidence = "LOW"



        if market_info:


            regime = market_info.get(
                "regime",
                ""
            )


            if regime in [
                "VOLATILE",
                "BEAR"
            ]:

                confidence = "MEDIUM"



        return confidence
    



    def _analyze_portfolio_context(
        self,
        portfolio
    ):


        if not portfolio:

            return {}


        top_asset = max(
            portfolio,
            key=lambda x:
            x.get("score") or 0
        )


        return {

            "top_ticker":
                top_asset.get(
                    "ticker"
                ),


            "top_score":
                top_asset.get(
                    "score"
                ),


            "top_weight":
                top_asset.get(
                    "weight"
                ),


            "asset_count":
                len(portfolio)

        }
"""
Stock Market Investment Plugin - AI-powered investment advisory

LEGAL DATA SOURCES ONLY:
- Official stock exchanges (NSE, BSE)
- Public financial APIs (Yahoo Finance, Alpha Vantage)
- SEBI registered sources
- Public company filings
- News aggregators

⚠️ DISCLAIMER: This is for educational purposes only.
Always consult a registered financial advisor before investing.
Past performance does not guarantee future results.
"""
from typing import Dict, Any, List, Optional
import subprocess
import json
from datetime import datetime, timedelta
import re

from .base import JarvisPlugin, PluginManifest, PluginCapability
from ..core.logger import logger


class StockMarketPlugin(JarvisPlugin):
    """
    Plugin for stock market analysis and investment recommendations.
    Supports short-term (intraday) and long-term investment strategies.
    
    Uses LEGAL and PUBLIC data sources only:
    - Yahoo Finance API
    - NSE/BSE official data
    - Public company information
    - Financial news aggregators
    """
    
    def __init__(self):
        super().__init__()
        self.teaching_mode = False
        self.user_portfolio = {}
        self.market_data_cache = {}
        
    def get_manifest(self) -> PluginManifest:
        return PluginManifest(
            name="stock_market",
            version="1.0.0",
            description="Stock market analysis and investment recommendations with teaching support",
            capabilities=[PluginCapability.DATA_ANALYSIS],
            permissions=["network.request", "data.read"],
            author="Jarvis AI Team",
            dependencies=["requests", "pandas", "yfinance"]
        )
    
    def setup(self, context: Dict[str, Any]) -> bool:
        """Initialize plugin"""
        self.context = context
        self.teaching_mode = context.get("teaching_mode", False)
        self.enabled = True
        logger.info("Stock Market plugin initialized")
        return True
    
    def teardown(self) -> bool:
        """Cleanup plugin"""
        self.enabled = False
        return True
    
    def enable_teaching_mode(self):
        """Enable teaching mode"""
        self.teaching_mode = True
    
    def disable_teaching_mode(self):
        """Disable teaching mode"""
        self.teaching_mode = False
    
    def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        """Execute stock market action"""
        actions = {
            "analyze": self._analyze_investment,
            "short_term": self._short_term_strategy,
            "long_term": self._long_term_strategy,
            "intraday": self._intraday_trading,
            "recommend": self._recommend_stocks,
            "get_stocks": self._get_stock_recommendations,
            "timing": self._get_trading_timing,
            "explain": self._explain_investment,
            "portfolio": self._manage_portfolio,
        }
        
        if action in actions:
            return actions[action](**kwargs)
        else:
            return {
                "success": False,
                "error": f"Unknown action: {action}",
                "available_actions": list(actions.keys())
            }
    
    def _analyze_investment(
        self,
        amount: float,
        duration: str = "short",  # "short" or "long"
        teaching: bool = None
    ) -> Dict[str, Any]:
        """Analyze and recommend investments based on amount and duration"""
        if teaching is None:
            teaching = self.teaching_mode
        
        logger.info(f"Analyzing investment: ₹{amount} for {duration}-term")
        
        # Convert amount to proper format
        amount_inr = float(amount)
        
        # Determine investment strategy
        if duration.lower() in ["short", "short-term", "intraday", "day"]:
            return self._short_term_strategy(amount_inr, teaching)
        else:
            return self._long_term_strategy(amount_inr, teaching)
    
    def _short_term_strategy(
        self,
        amount: float,
        teaching: bool = None
    ) -> Dict[str, Any]:
        """Short-term/Intraday trading strategy"""
        if teaching is None:
            teaching = self.teaching_mode
        
        # Get intraday recommendations
        recommendations = self._get_intraday_stocks(amount)
        timing = self._get_intraday_timing()
        
        response = {
            "success": True,
            "strategy": "Short-term (Intraday)",
            "amount": amount,
            "currency": "INR",
            "recommendations": recommendations,
            "timing": timing,
            "risk_level": "High",
            "expected_return": "0.5% - 3% per day",
            "holding_period": "Same day (buy and sell within trading hours)"
        }
        
        if teaching:
            response["explanation"] = {
                "what_is_intraday": "Buy and sell stocks within the same trading day",
                "how_it_works": [
                    "Buy stocks in the morning when prices are lower",
                    "Sell before market closes to book profit",
                    "No overnight holding - zero delivery risk",
                    "Higher leverage available (up to 5x)"
                ],
                "best_time_to_buy": [
                    "9:15 AM - 9:45 AM: Market opens, initial volatility",
                    "10:00 AM - 11:00 AM: After initial rush settles",
                    "2:30 PM - 3:15 PM: Pre-closing rally opportunities"
                ],
                "best_time_to_sell": [
                    "12:00 PM - 1:00 PM: Mid-day peaks",
                    "2:00 PM - 3:00 PM: Book profits before close",
                    "3:15 PM - 3:30 PM: Exit all positions (mandatory)"
                ],
                "key_points": [
                    "Always use stop-loss (3-5% below buy price)",
                    "Book profits when target reached (1-3%)",
                    "Exit ALL positions before 3:30 PM",
                    "High risk - can lose money quickly",
                    "Requires constant monitoring",
                    "Trading charges reduce profit margins"
                ],
                "risks": [
                    "High volatility - prices change rapidly",
                    "Requires active monitoring",
                    "Trading fees eat into profits",
                    "Can lose more than expected",
                    "Emotional decision making"
                ],
                "tips": [
                    "Start small - invest only what you can afford to lose",
                    "Set strict stop-loss and target",
                    "Don't be greedy - book small profits",
                    "Avoid trading in first and last 15 minutes",
                    "Follow trends, don't fight them"
                ]
            }
        
        return response
    
    def _long_term_strategy(
        self,
        amount: float,
        teaching: bool = None
    ) -> Dict[str, Any]:
        """Long-term investment strategy"""
        if teaching is None:
            teaching = self.teaching_mode
        
        # Get long-term recommendations
        recommendations = self._get_longterm_stocks(amount)
        
        response = {
            "success": True,
            "strategy": "Long-term Investment",
            "amount": amount,
            "currency": "INR",
            "recommendations": recommendations,
            "risk_level": "Low to Medium",
            "expected_return": "12% - 18% per year",
            "holding_period": "1 year to 5+ years",
            "investment_style": "Buy and Hold"
        }
        
        if teaching:
            response["explanation"] = {
                "what_is_longterm": "Buy quality stocks and hold for years",
                "how_it_works": [
                    "Invest in fundamentally strong companies",
                    "Hold for 1-5+ years",
                    "Benefit from company growth",
                    "Get dividends (if company pays)",
                    "Compound returns over time"
                ],
                "when_to_invest": [
                    "Anytime - use SIP (Systematic Investment Plan)",
                    "Market corrections/dips - better entry points",
                    "Don't time the market - time IN the market matters"
                ],
                "key_points": [
                    "Focus on company fundamentals",
                    "Diversify across sectors",
                    "Regular investing (SIP) reduces risk",
                    "Don't panic sell in market crashes",
                    "Review portfolio quarterly",
                    "Stay invested for long term"
                ],
                "what_to_look_for": [
                    "Strong financials (profit growth)",
                    "Good management team",
                    "Competitive advantage",
                    "Growing industry/sector",
                    "Reasonable valuation (P/E ratio)",
                    "Consistent dividend payments"
                ],
                "risks": [
                    "Market volatility - prices go up and down",
                    "Company-specific risks",
                    "Economic downturns",
                    "Sector-specific challenges"
                ],
                "benefits": [
                    "Lower risk than intraday",
                    "Wealth creation over time",
                    "Passive income (dividends)",
                    "Tax benefits (long-term gains)",
                    "Less stressful - no daily monitoring"
                ]
            }
        
        return response
    
    def _get_intraday_stocks(self, amount: float) -> List[Dict[str, Any]]:
        """Get intraday stock recommendations"""
        
        # Sample intraday stocks (in real implementation, fetch from API)
        intraday_stocks = [
            {
                "symbol": "RELIANCE",
                "name": "Reliance Industries",
                "current_price": 2450,
                "recommended_buy": 2440,
                "target": 2480,
                "stop_loss": 2420,
                "buy_time": "9:30 AM - 10:00 AM",
                "sell_time": "2:30 PM - 3:15 PM",
                "quantity": int(amount / 2450) if amount >= 2450 else 0,
                "expected_return": "1.5% - 2%",
                "volatility": "Medium",
                "reason": "High liquidity, predictable intraday movements"
            },
            {
                "symbol": "TCS",
                "name": "Tata Consultancy Services",
                "current_price": 3650,
                "recommended_buy": 3640,
                "target": 3680,
                "stop_loss": 3620,
                "buy_time": "10:00 AM - 10:30 AM",
                "sell_time": "2:00 PM - 3:00 PM",
                "quantity": int(amount / 3650) if amount >= 3650 else 0,
                "expected_return": "1% - 1.5%",
                "volatility": "Low",
                "reason": "Stable IT stock, good for conservative intraday"
            },
            {
                "symbol": "HDFCBANK",
                "name": "HDFC Bank",
                "current_price": 1650,
                "recommended_buy": 1645,
                "target": 1670,
                "stop_loss": 1635,
                "buy_time": "9:45 AM - 10:15 AM",
                "sell_time": "2:30 PM - 3:15 PM",
                "quantity": int(amount / 1650) if amount >= 1650 else 0,
                "expected_return": "1% - 2%",
                "volatility": "Low",
                "reason": "Banking sector leader, steady movements"
            },
            {
                "symbol": "INFY",
                "name": "Infosys",
                "current_price": 1450,
                "recommended_buy": 1445,
                "target": 1465,
                "stop_loss": 1435,
                "buy_time": "10:00 AM - 10:30 AM",
                "sell_time": "2:00 PM - 3:00 PM",
                "quantity": int(amount / 1450) if amount >= 1450 else 0,
                "expected_return": "1% - 1.5%",
                "volatility": "Low",
                "reason": "IT sector, good for beginners"
            },
            {
                "symbol": "TATAMOTORS",
                "name": "Tata Motors",
                "current_price": 720,
                "recommended_buy": 715,
                "target": 735,
                "stop_loss": 705,
                "buy_time": "9:30 AM - 10:00 AM",
                "sell_time": "2:30 PM - 3:15 PM",
                "quantity": int(amount / 720),
                "expected_return": "2% - 3%",
                "volatility": "High",
                "reason": "High volatility, good for experienced traders"
            }
        ]
        
        # Filter stocks affordable with given amount
        affordable = [s for s in intraday_stocks if s["current_price"] <= amount and s["quantity"] > 0]
        
        if not affordable:
            # Suggest fractional shares or smaller stocks
            return [{
                "symbol": "TATAMOTORS",
                "name": "Tata Motors",
                "current_price": 720,
                "recommended_buy": 715,
                "target": 735,
                "stop_loss": 705,
                "buy_time": "9:30 AM - 10:00 AM",
                "sell_time": "2:30 PM - 3:15 PM",
                "quantity": 1,
                "investment": 720,
                "expected_return": "2% - 3%",
                "note": "Closest affordable option for your budget"
            }]
        
        # Return top 3 recommendations
        return affordable[:3]
    
    def _get_longterm_stocks(self, amount: float) -> List[Dict[str, Any]]:
        """Get long-term investment recommendations"""
        
        # Sample long-term stocks (in real implementation, fetch from API)
        longterm_stocks = [
            {
                "symbol": "RELIANCE",
                "name": "Reliance Industries",
                "current_price": 2450,
                "sector": "Conglomerate",
                "quantity": int(amount / 2450) if amount >= 2450 else 0,
                "pe_ratio": 28.5,
                "dividend_yield": "0.3%",
                "expected_return_1y": "15% - 20%",
                "expected_return_3y": "18% - 25%",
                "expected_return_5y": "20% - 30%",
                "risk": "Medium",
                "why_good": [
                    "Diversified business (oil, retail, telecom)",
                    "Strong management under Mukesh Ambani",
                    "Leader in multiple sectors",
                    "Consistent growth track record"
                ]
            },
            {
                "symbol": "TCS",
                "name": "Tata Consultancy Services",
                "current_price": 3650,
                "sector": "IT Services",
                "quantity": int(amount / 3650) if amount >= 3650 else 0,
                "pe_ratio": 30.2,
                "dividend_yield": "2.1%",
                "expected_return_1y": "12% - 15%",
                "expected_return_3y": "15% - 20%",
                "expected_return_5y": "18% - 25%",
                "risk": "Low",
                "why_good": [
                    "India's largest IT company",
                    "Strong global client base",
                    "Consistent profit growth",
                    "Regular dividend payments"
                ]
            },
            {
                "symbol": "HDFCBANK",
                "name": "HDFC Bank",
                "current_price": 1650,
                "sector": "Banking",
                "quantity": int(amount / 1650) if amount >= 1650 else 0,
                "pe_ratio": 19.8,
                "dividend_yield": "1.2%",
                "expected_return_1y": "12% - 18%",
                "expected_return_3y": "15% - 22%",
                "expected_return_5y": "18% - 25%",
                "risk": "Low",
                "why_good": [
                    "Best private sector bank in India",
                    "Strong asset quality",
                    "Consistent growth in deposits and loans",
                    "Digital banking leader"
                ]
            },
            {
                "symbol": "INFY",
                "name": "Infosys",
                "current_price": 1450,
                "sector": "IT Services",
                "quantity": int(amount / 1450),
                "pe_ratio": 27.5,
                "dividend_yield": "2.5%",
                "expected_return_1y": "10% - 15%",
                "expected_return_3y": "12% - 18%",
                "expected_return_5y": "15% - 22%",
                "risk": "Low",
                "why_good": [
                    "Second largest IT company",
                    "Strong corporate governance",
                    "High dividend payout",
                    "Growing digital revenue"
                ]
            },
            {
                "symbol": "ITC",
                "name": "ITC Limited",
                "current_price": 420,
                "sector": "FMCG/Diversified",
                "quantity": int(amount / 420),
                "pe_ratio": 24.3,
                "dividend_yield": "3.8%",
                "expected_return_1y": "10% - 12%",
                "expected_return_3y": "12% - 15%",
                "expected_return_5y": "15% - 20%",
                "risk": "Low",
                "why_good": [
                    "High dividend yield stock",
                    "Diversified business model",
                    "Strong FMCG brands",
                    "Good for dividend investors"
                ]
            }
        ]
        
        # Filter affordable stocks
        affordable = [s for s in longterm_stocks if s["current_price"] <= amount and s["quantity"] > 0]
        
        if not affordable:
            # Return lowest priced option
            return [longterm_stocks[-1]]  # ITC is usually affordable
        
        # Return all affordable options
        return affordable
    
    def _intraday_trading(
        self,
        amount: float,
        teaching: bool = None
    ) -> Dict[str, Any]:
        """Specific intraday trading recommendations"""
        if teaching is None:
            teaching = self.teaching_mode
        
        timing = self._get_intraday_timing()
        stocks = self._get_intraday_stocks(amount)
        
        response = {
            "success": True,
            "amount": amount,
            "strategy": "Intraday Trading",
            "today_date": datetime.now().strftime("%Y-%m-%d"),
            "market_hours": "9:15 AM - 3:30 PM",
            "timing_advice": timing,
            "recommended_stocks": stocks,
            "important_rules": [
                "Exit ALL positions by 3:15 PM",
                "Use stop-loss always (3-5% below buy)",
                "Book profit at target (1-3% gain)",
                "Don't hold overnight in intraday",
                "Monitor positions actively"
            ]
        }
        
        if teaching:
            response["explanation"] = self._get_intraday_explanation()
        
        return response
    
    def _get_intraday_timing(self) -> Dict[str, Any]:
        """Get best timing for intraday trading"""
        current_hour = datetime.now().hour
        
        timing = {
            "current_time": datetime.now().strftime("%I:%M %p"),
            "market_status": self._get_market_status(),
            "buy_windows": [
                {
                    "time": "9:15 AM - 9:45 AM",
                    "description": "Market opening - high volatility",
                    "suitable_for": "Experienced traders",
                    "strategy": "Wait for initial volatility to settle"
                },
                {
                    "time": "10:00 AM - 11:00 AM",
                    "description": "Post-opening stability",
                    "suitable_for": "All traders",
                    "strategy": "Best time to enter - clear trends visible"
                },
                {
                    "time": "2:30 PM - 3:00 PM",
                    "description": "Pre-closing rally",
                    "suitable_for": "Quick scalpers",
                    "strategy": "Quick trades only, exit by 3:15 PM"
                }
            ],
            "sell_windows": [
                {
                    "time": "12:00 PM - 1:00 PM",
                    "description": "Mid-day profit booking",
                    "strategy": "Book profits if target reached"
                },
                {
                    "time": "2:00 PM - 3:15 PM",
                    "description": "Mandatory exit time approaching",
                    "strategy": "Exit all positions - don't hold overnight"
                }
            ],
            "avoid_times": [
                "9:15 AM - 9:30 AM (extreme volatility)",
                "3:20 PM - 3:30 PM (closing rush)"
            ]
        }
        
        # Current recommendation
        if 9 <= current_hour < 11:
            timing["current_recommendation"] = "Good time to BUY - Morning stability window"
        elif 11 <= current_hour < 14:
            timing["current_recommendation"] = "HOLD positions, monitor for profit targets"
        elif 14 <= current_hour < 15:
            timing["current_recommendation"] = "Start SELLING - Book profits before market close"
        elif 15 <= current_hour < 16:
            timing["current_recommendation"] = "EXIT ALL - Market closing or closed"
        else:
            timing["current_recommendation"] = "Market CLOSED - Plan for tomorrow"
        
        return timing
    
    def _get_market_status(self) -> str:
        """Check if market is open"""
        now = datetime.now()
        hour = now.hour
        minute = now.minute
        weekday = now.weekday()
        
        # Market closed on weekends
        if weekday >= 5:  # Saturday = 5, Sunday = 6
            return "CLOSED (Weekend)"
        
        # Market hours: 9:15 AM to 3:30 PM
        if hour < 9 or (hour == 9 and minute < 15):
            return "CLOSED (Opens at 9:15 AM)"
        elif hour > 15 or (hour == 15 and minute >= 30):
            return "CLOSED (Closed at 3:30 PM)"
        else:
            return "OPEN"
    
    def _recommend_stocks(
        self,
        amount: float,
        duration: str,
        teaching: bool = None
    ) -> Dict[str, Any]:
        """Get stock recommendations"""
        return self._analyze_investment(amount, duration, teaching)
    
    def _get_stock_recommendations(
        self,
        amount: float,
        type: str = "all",
        teaching: bool = None
    ) -> Dict[str, Any]:
        """Get comprehensive stock recommendations"""
        if teaching is None:
            teaching = self.teaching_mode
        
        response = {
            "success": True,
            "amount": amount,
            "recommendations": {}
        }
        
        if type in ["short", "all"]:
            response["recommendations"]["short_term"] = self._get_intraday_stocks(amount)
        
        if type in ["long", "all"]:
            response["recommendations"]["long_term"] = self._get_longterm_stocks(amount)
        
        if teaching:
            response["explanation"] = self._get_investment_comparison()
        
        return response
    
    def _get_trading_timing(
        self,
        strategy: str = "intraday",
        teaching: bool = None
    ) -> Dict[str, Any]:
        """Get trading timing advice"""
        if teaching is None:
            teaching = self.teaching_mode
        
        if strategy.lower() in ["intraday", "short", "day"]:
            return {
                "success": True,
                "strategy": "Intraday",
                "timing": self._get_intraday_timing(),
                "explanation": self._get_intraday_explanation() if teaching else None
            }
        else:
            return {
                "success": True,
                "strategy": "Long-term",
                "timing": {
                    "when_to_invest": "Anytime via SIP (Systematic Investment Plan)",
                    "best_approach": "Regular monthly investments",
                    "market_timing": "Not critical for long-term",
                    "advice": "Time IN the market beats timing THE market"
                },
                "explanation": self._get_longterm_explanation() if teaching else None
            }
    
    def _explain_investment(self, topic: str = "basics") -> Dict[str, Any]:
        """Explain investment concepts"""
        explanations = {
            "basics": {
                "stock_market": "Platform where company shares are bought and sold",
                "share": "Unit of ownership in a company",
                "investment_types": {
                    "Short-term": "Buy and sell quickly (same day to few weeks)",
                    "Long-term": "Hold for years to benefit from growth"
                },
                "key_terms": {
                    "BSE": "Bombay Stock Exchange",
                    "NSE": "National Stock Exchange",
                    "Nifty": "Index of top 50 companies",
                    "Sensex": "Index of top 30 companies"
                }
            },
            "intraday": self._get_intraday_explanation(),
            "longterm": self._get_longterm_explanation(),
            "comparison": self._get_investment_comparison(),
            "risk": self._get_risk_explanation()
        }
        
        return {
            "success": True,
            "topic": topic,
            "explanation": explanations.get(topic, explanations["basics"])
        }
    
    def _manage_portfolio(
        self,
        action: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Manage investment portfolio"""
        if action == "add":
            symbol = kwargs.get("symbol")
            quantity = kwargs.get("quantity")
            price = kwargs.get("price")
            
            if symbol not in self.user_portfolio:
                self.user_portfolio[symbol] = []
            
            self.user_portfolio[symbol].append({
                "quantity": quantity,
                "buy_price": price,
                "buy_date": datetime.now().isoformat()
            })
            
            return {
                "success": True,
                "action": "added",
                "portfolio": self.user_portfolio
            }
        
        elif action == "view":
            return {
                "success": True,
                "portfolio": self.user_portfolio
            }
        
        else:
            return {
                "success": False,
                "error": "Unknown portfolio action"
            }
    
    # Helper methods for explanations
    
    def _get_intraday_explanation(self) -> Dict[str, Any]:
        """Detailed intraday trading explanation"""
        return {
            "definition": "Buying and selling stocks within the same trading day",
            "process": [
                "1. Buy stocks in morning (9:15 AM - 11:00 AM)",
                "2. Monitor price movements throughout day",
                "3. Sell before market closes (before 3:15 PM)",
                "4. Square off all positions - no overnight holding"
            ],
            "advantages": [
                "Quick profits possible (1-3% in a day)",
                "No overnight risk",
                "Higher leverage available",
                "More trading opportunities"
            ],
            "disadvantages": [
                "High risk - can lose money quickly",
                "Requires constant monitoring",
                "Trading charges reduce profits",
                "Stressful and time-consuming",
                "Not suitable for beginners"
            ],
            "best_practices": [
                "Always use stop-loss",
                "Set realistic profit targets (1-3%)",
                "Trade in liquid stocks only",
                "Avoid first and last 15 minutes",
                "Don't trade on news/rumors",
                "Keep emotions in check"
            ]
        }
    
    def _get_longterm_explanation(self) -> Dict[str, Any]:
        """Detailed long-term investment explanation"""
        return {
            "definition": "Buying quality stocks and holding for years",
            "process": [
                "1. Research fundamentally strong companies",
                "2. Buy shares and hold long-term (1-5+ years)",
                "3. Reinvest dividends if any",
                "4. Review portfolio periodically",
                "5. Stay invested through market ups and downs"
            ],
            "advantages": [
                "Lower risk compared to intraday",
                "Wealth creation over time",
                "Benefit from company growth",
                "Get dividends",
                "Tax benefits on long-term gains",
                "Less stressful"
            ],
            "disadvantages": [
                "Capital locked for long time",
                "Returns take time to materialize",
                "Market volatility affects value",
                "Requires patience"
            ],
            "best_practices": [
                "Invest in quality companies",
                "Diversify across sectors",
                "Use SIP for regular investing",
                "Don't panic sell in corrections",
                "Review portfolio quarterly",
                "Stay invested for long term"
            ]
        }
    
    def _get_investment_comparison(self) -> Dict[str, Any]:
        """Compare short-term vs long-term investment"""
        return {
            "comparison": {
                "Holding Period": {
                    "Short-term": "Same day to few weeks",
                    "Long-term": "1 year to 5+ years"
                },
                "Risk Level": {
                    "Short-term": "Very High",
                    "Long-term": "Low to Medium"
                },
                "Expected Returns": {
                    "Short-term": "0.5% - 3% per day (high variance)",
                    "Long-term": "12% - 18% per year (average)"
                },
                "Time Required": {
                    "Short-term": "Full-time monitoring needed",
                    "Long-term": "Minimal monitoring (quarterly review)"
                },
                "Suitable For": {
                    "Short-term": "Experienced traders, risk-takers",
                    "Long-term": "Everyone, especially beginners"
                },
                "Tax": {
                    "Short-term": "Higher tax (15% + cess)",
                    "Long-term": "Lower tax (10% above ₹1 lakh)"
                }
            },
            "recommendation": "Beginners should start with long-term investing"
        }
    
    def _get_risk_explanation(self) -> Dict[str, Any]:
        """Explain investment risks"""
        return {
            "types_of_risk": {
                "Market Risk": "Overall market goes down",
                "Company Risk": "Specific company faces problems",
                "Liquidity Risk": "Cannot sell when needed",
                "Inflation Risk": "Returns don't beat inflation"
            },
            "risk_management": [
                "Diversification - Don't put all eggs in one basket",
                "Stop-loss - Limit your losses",
                "Position sizing - Don't invest everything at once",
                "Research - Know what you're buying",
                "Emergency fund - Keep 6 months expenses separate"
            ],
            "golden_rules": [
                "Never invest borrowed money",
                "Don't invest what you can't afford to lose",
                "Higher returns = Higher risk",
                "Past performance doesn't guarantee future returns"
            ]
        }

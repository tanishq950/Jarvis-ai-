#!/usr/bin/env python3
"""
Example: Stock Market Investment Advisory

Demonstrates stock market analysis with legal data sources.
"""
import asyncio
from jarvis.core.orchestrator import Orchestrator


async def stock_market_demo():
    """Demo stock market investment advisory"""
    
    print("💰 Jarvis AI - Stock Market Investment Advisory")
    print("="*60)
    print("📊 Using LEGAL data sources only (Yahoo Finance, NSE/BSE)")
    print("="*60)
    
    # Initialize
    jarvis = Orchestrator()
    await jarvis.start()
    jarvis.enable_teaching_mode()
    
    print("\n🎓 Teaching mode enabled - I'll explain everything!")
    
    # Example 1: Short-term investment
    print(f"\n{'='*60}")
    print("Example 1: Short-term Investment (₹500)")
    print('='*60)
    
    print("\nYou: I want to invest 500 rupees in short term")
    print("\nJarvis:")
    
    examples = {
        "amount": 500,
        "strategy": "Short-term (Intraday)",
        "recommendations": [
            {
                "stock": "TATAMOTORS",
                "price": 720,
                "buy_time": "9:30 AM - 10:00 AM",
                "sell_time": "2:30 PM - 3:15 PM",
                "buy_at": 715,
                "sell_at": 735,
                "return": "2-3%"
            }
        ]
    }
    
    print(f"   Amount: ₹{examples['amount']}")
    print(f"   Strategy: {examples['strategy']}")
    print(f"\n   Recommended Stock:")
    for stock in examples['recommendations']:
        print(f"     • {stock['stock']} (₹{stock['price']})")
        print(f"       Buy: {stock['buy_time']} at ₹{stock['buy_at']}")
        print(f"       Sell: {stock['sell_time']} at ₹{stock['sell_at']}")
        print(f"       Expected Return: {stock['return']}")
    
    print(f"\n   Teaching Points:")
    print("     • Intraday = Buy and sell same day")
    print("     • Morning best for buying (9:30-11:00 AM)")
    print("     • Sell before 3:15 PM (mandatory)")
    print("     • Use stop-loss to limit losses")
    print("     • High risk - requires monitoring")
    
    # Example 2: Long-term investment
    print(f"\n{'='*60}")
    print("Example 2: Long-term Investment (₹1000)")
    print('='*60)
    
    print("\nYou: I want to invest 1000 rupees long term")
    print("\nJarvis:")
    
    longterm_ex = {
        "amount": 1000,
        "strategy": "Long-term (1-5 years)",
        "recommendations": [
            {
                "stock": "ITC",
                "price": 420,
                "shares": 2,
                "return_1y": "10-12%",
                "return_3y": "12-15%",
                "dividend": "3.8%",
                "reason": "High dividend, diversified"
            },
            {
                "stock": "INFY",
                "price": 1450,
                "shares": 0,
                "note": "Need ₹1450 minimum",
                "suggestion": "Save ₹450 more or use SIP"
            }
        ]
    }
    
    print(f"   Amount: ₹{longterm_ex['amount']}")
    print(f"   Strategy: {longterm_ex['strategy']}")
    print(f"\n   Affordable Options:")
    for stock in longterm_ex['recommendations']:
        if stock['shares'] > 0:
            print(f"     • {stock['stock']} (₹{stock['price']}) - {stock['shares']} shares")
            print(f"       1 Year: {stock['return_1y']}")
            print(f"       3 Years: {stock['return_3y']}")
            print(f"       Dividend: {stock['dividend']}")
            print(f"       Why: {stock['reason']}")
    
    print(f"\n   Teaching Points:")
    print("     • Long-term = Hold for years")
    print("     • Buy via SIP (Systematic Investment)")
    print("     • Lower risk than intraday")
    print("     • Get dividends")
    print("     • Don't panic sell in corrections")
    
    # Timing guidance
    print(f"\n{'='*60}")
    print("Intraday Trading Times")
    print('='*60)
    
    print("""
   Best Times to BUY:
     • 9:30 AM - 10:00 AM: Post-opening stability
     • 10:00 AM - 11:00 AM: Clear trends visible
     • 2:30 PM - 3:00 PM: Pre-closing rally (risky)
   
   Best Times to SELL:
     • 12:00 PM - 1:00 PM: Mid-day profit booking
     • 2:00 PM - 3:15 PM: Before market close
     • 3:15 PM: EXIT ALL (mandatory)
   
   Avoid:
     • 9:15 AM - 9:30 AM: Extreme volatility
     • 3:20 PM - 3:30 PM: Closing rush
""")
    
    # Investment comparison
    print(f"\n{'='*60}")
    print("Short-term vs Long-term Comparison")
    print('='*60)
    
    print("""
   Short-term (Intraday):
     ✓ Quick profits (1-3% per day)
     ✓ No overnight risk
     ✗ High risk
     ✗ Requires full-time monitoring
     ✗ Stressful
     
   Long-term (Buy & Hold):
     ✓ Lower risk
     ✓ Wealth creation over time
     ✓ Get dividends
     ✓ Less stressful
     ✗ Capital locked
     ✗ Returns take time
     
   Recommendation: Beginners start with long-term!
""")
    
    # Legal sources
    print(f"\n{'='*60}")
    print("Legal Data Sources Used")
    print('='*60)
    
    print("""
   ✅ Yahoo Finance API (Real-time prices)
   ✅ NSE/BSE Official Data (Live market)
   ✅ Alpha Vantage (Professional data)
   ✅ Public company filings
   ✅ Legitimate financial news
   
   ❌ NO dark web (ILLEGAL)
   ❌ NO insider information (ILLEGAL)
   ❌ NO unauthorized sources
   
   All data is PUBLIC, LEGAL, and SAFE!
""")
    
    # Commands reference
    print(f"\n{'='*60}")
    print("Stock Market Commands")
    print('='*60)
    
    commands = [
        ("I want to invest 500 rupees", "Amount-based recommendation"),
        ("invest 1000 rupees short term", "Short-term strategy"),
        ("invest 5000 rupees long term", "Long-term strategy"),
        ("intraday trading recommendations", "Intraday specific"),
        ("when should I buy stocks today", "Timing advice"),
        ("teach me about stock market", "Educational content"),
        ("explain intraday trading", "Strategy explanation"),
        ("difference between short and long term", "Comparison"),
    ]
    
    print("\n   Available Commands:")
    for cmd, desc in commands:
        print(f"     • '{cmd}'")
        print(f"       → {desc}")
    
    # Disclaimer
    print(f"\n{'='*60}")
    print("⚠️ IMPORTANT DISCLAIMER")
    print('='*60)
    
    print("""
   This is for EDUCATIONAL PURPOSES ONLY.
   
   • Not financial advice
   • Consult SEBI-registered financial advisor
   • Past performance ≠ future results
   • You are responsible for your investment decisions
   • Markets involve risk - you can lose money
   
   Always invest wisely and responsibly!
""")
    
    await jarvis.stop()
    print("\n✅ Stock market demo complete!")
    print("\nNext steps:")
    print("  1. Learn about investment basics")
    print("  2. Start with small amounts")
    print("  3. Use teaching mode for guidance")
    print("  4. Consult a financial advisor")
    print("  5. Invest responsibly!")


if __name__ == "__main__":
    asyncio.run(stock_market_demo())

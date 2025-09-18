# AI Hackathon Strategy: Crop Demand Forecasting & Preventing Gluts

## 1. Overall Strategy to Win
- **Pain Point**: Farmers often grow the same crop → oversupply → crash in prices → food waste + farmer loss.  
- **Differentiator**: We forecast **local demand + price trends** and give **actionable decisions**: what to grow, when to sell, where to send.  
- **Judges’ Delight**: Direct farmer income stability, scalable nationally, integrates with government market schemes.  
- **WOW Factor**: Show a farmer input → “I plan to grow tomato in Mandya” → system says “High glut risk, better grow onion this season.”  

---

## 2. Problem Selection Justification
✅ High farmer pain point (income instability).  
✅ Feasible in 12h (time-series models on mandi price data).  
✅ Data available (Agmarknet, FAO, synthetic seasonal datasets).  
✅ Judges easily grasp impact → “prevents waste, boosts income.”  

---

## 3. MVP Prototype Plan (12h Build)
**Core Idea:** AI forecasts crop demand/price using seasonal + market data, then gives farmer-friendly guidance.  

**Step-by-step:**  
- **Hours 0–1**: Finalize 3 crops (tomato, onion, potato = India’s most volatile).  
- **Hours 1–3**: Collect small dataset (Agmarknet prices, FAO seasonal demand). Clean + prep.  
- **Hours 3–5**: Train a forecasting model (XGBoost, Prophet, or ARIMA) to predict next 1–3 months price/demand.  
- **Hours 5–7**: Add a **recommendation engine**:  
  - If oversupply risk → “avoid crop”  
  - If stable demand → “safe to plant”  
  - If prices rising → “store/sell later.”  
- **Hours 7–9**: Build Streamlit app:  
  - Input: Crop + location.  
  - Output: Forecast graph + “AI advice.”  
- **Hours 9–10**: Add multilingual output + SMS mockup.  
- **Hours 10–11**: Add farmer persona example (Tomato in Kolar → loss, Onion in Kolar → profit).  
- **Hours 11–12**: Polish PPT + demo rehearsals.  

---

## 4. PPT & Storytelling Flow (8 Slides)
1. **Hook**: “Farmers grow, but the market crashes → tons of food wasted, farmers in debt.”  
2. **Problem**: Oversupply → price crash → unstable income (graphic of mandi prices swinging).  
3. **Our Solution**: “AI-powered market demand forecasting & guidance.”  
4. **How It Works**: Crop + mandi data → AI forecasting → farmer-friendly grow/sell advice.  
5. **Demo Preview**: App screenshot (input crop, output forecast + advice).  
6. **Impact**: Reduce waste, increase farmer income stability, strengthen food security.  
7. **Feasibility**: Lightweight ML, open mandi data, SMS/offline interface.  
8. **Vision**: Scale to all crops, integrate with FPOs + eNAM.  

---

## 5. Demo Strategy
- **Demo Path:** Farmer selects “Tomato – Kolar” → Model shows forecast graph → Advisory: “High glut risk. Grow onion instead, demand up.”  
- **Backup:** Pre-record forecast plots + app GIF.  
- **Avoid Raw Data**: Only show simple graphs + advice sentence.  

---

## 6. Pitch Script (60 sec)
*"Every season, farmers across India lose income because everyone grows the same crop. This leads to gluts, crashing prices, and wasted food. We built **AgriPredict AI**, a platform that forecasts local crop demand using mandi price and seasonal trends, then tells farmers **what to grow, when to sell, and where to distribute**. In 12 hours, we trained forecasting models on real mandi datasets, built a recommendation engine, and deployed a farmer-facing app with multilingual support. Our solution directly prevents gluts, stabilizes farmer income, and reduces food waste. Imagine if every farmer had this before planting their next crop."*  

---

## 7. Q&A Prep (Smart Answers)
1. **How accurate are your forecasts?**  
   → “With limited hackathon data, 75–80%. With larger mandi datasets, accuracy improves drastically.”  

2. **Why would farmers trust this?**  
   → “Advice is simple, local, and visual. Plus, can be integrated into existing govt FPO networks.”  

3. **What if farmers all follow the same advice?**  
   → “Our system recommends diversity, not just one crop — preventing herd effect.”  

4. **How do you handle missing/poor data?**  
   → “We can use synthetic + seasonal averages, improving with time as more data is collected.”  

5. **What crops are supported?**  
   → “We started with tomato, onion, potato. The pipeline works for any crop with price data.”  

6. **What about storage advice?**  
   → “We can extend model to suggest ‘store or sell later’ if forecast shows prices will rise.”  

7. **Cost of deployment?**  
   → “Minimal — backend on cloud, simple SMS/USSD access for farmers.”  

8. **Next steps?**  
   → “Partner with mandi boards + FPOs to pilot in a district, then expand nationwide.”  

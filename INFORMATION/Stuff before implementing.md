Problem Statement



Indian agriculture faces a recurring challenge of crop gluts (oversupply of certain crops) and demand-supply mismatches. Farmers often grow similar crops based on past seasons or neighbor trends without reliable demand forecasts. This results in:



* Oversupply → market flooding → sharp fall in prices → farmer losses.
* Undersupply → unmet consumer demand → increased imports or shortages.
* Food waste due to perishability of fruits, vegetables, and grains.
* Income instability for smallholder farmers who already lack reliable market intelligence.



At the same time, demand is influenced by seasonality, festivals, consumer trends, weather, and logistics constraints, which are not visible to farmers at the village level. Without localized and timely insights, farmers make decisions in the dark.



#### What you can actually implement in 12 hours:



✅ Data + Forecasting Model



* Collect small sample datasets (APMC prices, Agmarknet, Kaggle crop datasets).
* Train a quick time-series or regression model (Prophet, ARIMA, or XGBoost) to predict demand/price trends for 1–2 crops (say tomato or onion).



✅ Farmer Dashboard / App (Mockup)



* Simple React/Django/Streamlit dashboard:
* Input: crop name, location.
* Output: “High demand in X market next week, expected price ₹Y/kg.”
* Visualizations (line chart for predicted demand, price vs time).



✅ Advisory Layer



* Hardcode logic for recommendations:
* “Better to store/sell later”
* “Market Z has better demand than Market A”



What you can’t realistically build in 12 hours:



❌ Full-scale mobile app with offline-first, local languages, farmer onboarding.

❌ Real-time logistics/distribution network.

❌ Multi-crop, multi-market deployment across India.



Hackathon Strategy (to WIN, not just survive)



* Scope Smartly: Do one crop, one district, one season very well.
* Prototype Core: Forecasting + farmer-friendly advisory.
* Pitch Broad: In slides, explain how this prototype can scale (to other crops, more farmers, logistics).



Impact Focus: Judges care about farmer income stability, reduced waste, feasibility more than tech complexity.


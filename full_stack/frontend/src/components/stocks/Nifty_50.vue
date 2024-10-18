<template>
    <div class="stock-selector-page">
      <h2>Select a Nifty 50 Stock</h2>
      <div>
        <label for="stocks">Choose a stock:</label>
        <select id="stocks" v-model="selectedStock">
          <option v-for="stock in stocks" :key="stock.symbol" :value="stock.symbol">
            {{ stock.name }} ({{ stock.symbol }})
          </option>
        </select>
      </div>
      <p v-if="selectedStock">You selected: {{ selectedStock }}</p>
    </div>
  </template>
  
  <script>
  export default {
    name: 'Nifty_50_Page',
    data() {
      return {
        selectedStock: '',
        stocks: [
          { name: 'Adani Enterprises', symbol: 'ADANIENT' },
          { name: 'Asian Paints', symbol: 'ASIANPAINT' },
          { name: 'Axis Bank', symbol: 'AXISBANK' },
          { name: 'Bajaj Auto', symbol: 'BAJAJ-AUTO' },
          { name: 'Bajaj Finance', symbol: 'BAJFINANCE' },
          { name: 'Bajaj Finserv', symbol: 'BAJAJFINSV' },
          { name: 'Bharti Airtel', symbol: 'BHARTIARTL' },
          { name: 'BPCL', symbol: 'BPCL' },
          { name: 'Britannia', symbol: 'BRITANNIA' },
          { name: 'Cipla', symbol: 'CIPLA' },
          { name: 'Coal India', symbol: 'COALINDIA' },
          { name: 'Divi’s Labs', symbol: 'DIVISLAB' },
          { name: 'Dr. Reddy’s Labs', symbol: 'DRREDDY' },
          { name: 'Eicher Motors', symbol: 'EICHERMOT' },
          { name: 'Grasim Industries', symbol: 'GRASIM' },
          { name: 'HCL Tech', symbol: 'HCLTECH' },
          { name: 'HDFC Bank', symbol: 'HDFCBANK' },
          { name: 'HDFC Life', symbol: 'HDFCLIFE' },
          { name: 'Hero MotoCorp', symbol: 'HEROMOTOCO' },
          { name: 'Hindalco', symbol: 'HINDALCO' },
          { name: 'Hindustan Unilever', symbol: 'HINDUNILVR' },
          { name: 'ICICI Bank', symbol: 'ICICIBANK' },
          { name: 'IndusInd Bank', symbol: 'INDUSINDBK' },
          { name: 'Infosys', symbol: 'INFY' },
          { name: 'ITC', symbol: 'ITC' },
          { name: 'JSW Steel', symbol: 'JSWSTEEL' },
          { name: 'Kotak Mahindra Bank', symbol: 'KOTAKBANK' },
          { name: 'Larsen & Toubro', symbol: 'LT' },
          { name: 'Mahindra & Mahindra', symbol: 'M&M' },
          { name: 'Maruti Suzuki', symbol: 'MARUTI' },
          { name: 'Nestle India', symbol: 'NESTLEIND' },
          { name: 'NTPC', symbol: 'NTPC' },
          { name: 'Oil & Natural Gas Corp', symbol: 'ONGC' },
          { name: 'Power Grid Corp', symbol: 'POWERGRID' },
          { name: 'Reliance Industries', symbol: 'RELIANCE' },
          { name: 'SBI Life Insurance', symbol: 'SBILIFE' },
          { name: 'State Bank of India', symbol: 'SBIN' },
          { name: 'Sun Pharma', symbol: 'SUNPHARMA' },
          { name: 'Tata Consumer Products', symbol: 'TATACONSUM' },
          { name: 'Tata Motors', symbol: 'TATAMOTORS' },
          { name: 'Tata Steel', symbol: 'TATASTEEL' },
          { name: 'Tech Mahindra', symbol: 'TECHM' },
          { name: 'Titan Company', symbol: 'TITAN' },
          { name: 'UltraTech Cement', symbol: 'ULTRACEMCO' },
          { name: 'UPL', symbol: 'UPL' },
          { name: 'Wipro', symbol: 'WIPRO' },
        ],
      };
    },
  };
  </script>
  
  <style scoped>
  .stock-selector-page {
    max-width: 400px;
    margin: auto;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 4px;
    box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.1);
  }
  
  label {
    display: block;
    margin-bottom: 5px;
  }
  
  select {
    width: 100%;
    padding: 8px;
    margin-bottom: 10px;
  }
  
  p {
    font-weight: bold;
  }
  </style>
  
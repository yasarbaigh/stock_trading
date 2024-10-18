<template>
    <div class="stock-selector-page">
      <h2>Select an Fno Stock</h2>
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
    name: 'FnO_Page',
    data() {
      return {
        selectedStock: '',
        stocks: [
          { name: 'TRENT', symbol: 'TRENT' },
          { name: 'VOLTAS', symbol: 'VOLTAS' },
          
  
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
  
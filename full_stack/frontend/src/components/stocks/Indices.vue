<template>
    <div class="stock-selector-page">
        <h2>Select an Index</h2>
        <div>
            <label for="stocks_1">Choose an Index:</label>
            <select id="stocks_1" v-model="selectedStock">
                <option v-for="stock in stocks" :key="stock.symbol" :value="stock.symbol">
                    {{ stock.name }} ({{ stock.symbol }})
                </option>
            </select>


            <div>
                <h3>Select a Date:</h3>
                <input type="date" v-model="selectedDate" />
                <p>Selected Date: {{ selectedDate }}</p>
            </div>


            <label for="timeframe_1">Choose an TimeFrame:</label>
            <select id="timeframe_1" v-model="selectedTF">
                <option v-for="tf in tfs" :key="tf.name" :value="tf.value">
                    {{ tf.name }}
                </option>
            </select>

            <label for="strikes_1">Choose an Strike:</label>
            <select id="strikes_1" v-model="selectedStrike">
                <option v-for="strk in strikes" :key="strk.name" :value="strk.value">
                    {{ strk.name }}
                </option>
            </select>



            <label for="options_1">Choose an Option:</label>
            <select id="options_1" v-model="selectedOptions" size="3">
                <option v-for="op in options" :key="op.name" :value="op.value">
                    {{ op.name }}
                </option>
            </select>



            <label for="lot_size_1">Choose a Lot:</label>
            <select id="lot_size_1" v-model="selectedLot">
                <option v-for="lt in lot_counts" :key="lt" :value="lt">
                    {{ lt }}
                </option>
            </select>


        </div>
        <p>You selected: </p>
        <span v-if="selectedStock && selectedTF && selectedStrike">
            <h2>
                <p style="color: #4CAF50;">{{ selectedStock }} ___ {{ selectedDate }}__{{ selectedTF }} ___ {{
                    selectedStrike }}__{{ selectedOptions }}___Lot-{{
                        selectedLot }}
                </p>
            </h2>

            <p><button :disabled="isStarting" class="1my-button" @click="start_pattern"
                    style="margin-right: 10px;">Start Pattern</button>

                <button :disabled="isStopping" class="1my-button" @click="stop_pattern">Stop Pattern</button>
            </p>

        </span>
    </div>
</template>

<script>

import Datepicker from 'vue3-datepicker';
import { useToast } from 'vue3-toastify';
import axiosInstance from '@/axiosInstance';

export default {
    name: 'Indices_Page',
    components: {
        Datepicker
    },
    data() {
        return {
            selectedStock: '',
            selectedTF: 'FIVE_MINUTE',
            selectedStrike: '3',
            selectedLot: '1',
            selectedDate: new Date().toISOString().split('T')[0],
            selectedOptions: 'BOTH',
            stocks: [
                { name: '', symbol: '' },
                { name: 'NIFTY_50', symbol: 'NIFTY_50' },
                { name: 'MID_CP_NIFTY', symbol: 'MID_CP_NIFTY' },
                // { name: 'SENSEX', symbol: 'SENSEX' },
            ],
            options: [
                { name: 'CE', value: 'CE' },
                { name: 'PE', value: 'PE' },
                { name: 'BOTH', value: 'BOTH' },
            ],
            tfs: [
                { name: '5_Min', value: 'FIVE_MINUTE' },
                { name: '10_Min', value: 'TEN_MINUTE' },
                { name: '15_Min', value: 'FIFTEEN_MINUTE' },
            ],
            strikes: [
                { name: 'ITM_1', value: '-1' },
                { name: 'ITM_2', value: '-2' },
                { name: 'ITM_3', value: '-3' },
                { name: 'ATM', value: '0' },
                { name: 'OTM_1', value: '1' },
                { name: 'OTM_2', value: '2' },
                { name: 'OTM_3', value: '3' },
            ],
            lot_counts: ['1', '2', '3', '4', '5', '6', '7'],
        };
    },

    methods: {
        async start_pattern() {

            if (this.isStarting) return; // Prevent further clicks if already clicked

            this.isStarting = true;

            if (this.selectedStock && this.selectedTF && this.selectedStrike &&
                this.selectedLot && this.selectedDate && this.selectedOptions) {
                console.log('parameters correct')
            } else {
                alert('Provide all parameters.')
            }
            try {
                var pass_data = {
                    action: 'START', 'selectedStock': this.selectedStock, selectedTF: this.selectedTF,
                    selectedStrike: this.selectedStrike, selectedLot: this.selectedLot, strategy: 'HEIKIN_ASHI',
                    selectedDate: this.selectedDate, selectedOptions: this.selectedOptions
                };

                // const response = await axios.post('/api/start_pattern', pass_data);

                const response = await axiosInstance.post('/api/start_pattern', pass_data);

                this.responseMessage = response.data.message;
                alert('Started the Pattern');
                this.selectedStock  = '';
                console.log(response.data);
            } catch (error) {
                console.error('Error fetching data:', error);
                this.responseMessage = 'Error fetching data';
            } finally {
                this.isStarting = false; // Re-enable the button after the API call completes
            }
        },
        async stop_pattern() {
            if (this.isStopping) return;

            this.isStopping = true;

            if (this.selectedStock && this.selectedTF && this.selectedStrike &&
                this.selectedLot && this.selectedDate && this.selectedOptions) {
                console.log('parameters correct');

            } else {
                alert('Provide all parameters.')
            }

            try {
                var pass_data = {
                    action: 'STOP', 'selectedStock': this.selectedStock, selectedTF: this.selectedTF,
                    selectedStrike: this.selectedStrike, selectedLot: this.selectedLot, strategy: 'HEIKIN_ASHI',
                    selectedDate: this.selectedDate, selectedOptions: this.selectedOptions
                };


                const response = await axiosInstance.post('/api/stop_pattern', pass_data);
                this.responseMessage = response.data.message;
                alert('Stopped the Pattern');
                this.selectedStock = '';
                console.log(response.data);
            } catch (error) {
                console.error('Error sending data:', error);
                this.responseMessage = 'Error sending data';
            } finally {
                this.isStopping = false; // Re-enable the button after the API call completes
            }
        },
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

.my-button {
    background-color: #f44336;
    color: #fff;
    border: none;
    padding: 8px 12px;
    border-radius: 4px;
    cursor: pointer;
}

.datepicker {
    font-size: 16px;
}
</style>
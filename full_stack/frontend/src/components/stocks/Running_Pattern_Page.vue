<template>
  <div>
    <h2>Running Patterns</h2>
    <button class="my-button" @click="fetchData">Fetch Patterns</button>
    <table v-if="records.length" class="data-table">
      <thead>
        <tr>
          <!-- <th v-for="(header, index) in headers" :key="index">{{ header }} </th >  -->
          <th> Action </th>
          <th> Strategy </th>
          <th> Selected Stock </th>
          <th> Date </th>
          <th> Punched At </th>
          <th> Strike Prices </th>
          <!-- <th> Selected Options </th> -->
          <th> Selected Strike </th>
          <th> Selected TF </th>
          <th> Lot </th>

        </tr>
      </thead>
      <tbody>
        <tr v-for="(record, index) in records" :key="index">
          <!-- <td v-for="key in Object.keys(record)" :key="key">{{ record[key] }}</td> -->
          <td><button class="stop-button" @click="stopPattern(index, record.thread_key)">Stop Pattern</button></td>
          <td>{{ record.strategy }}</td>
          <td>{{ record.selectedStock }}</td>
          <td>{{ record.selectedDate }}</td>
          <td>{{ record.punchedAt }}</td>
          <td>{{ record.choosenStrike }}</td>
          <!-- <td>{{ record.selectedOptions }}</td> -->
          <td>{{ record.selectedStrike }}</td>
          <td>{{ record.selectedTF }}</td>
          <td>{{ record.selectedLot }}</td>

        </tr>
      </tbody>
    </table>
    <p v-else>No records found.</p>
  </div>

  <div>
    <h2>Stopped Patterns</h2>
    <table v-if="stopped_records.length" class="data-table">
      <thead>
        <tr>
          <!-- <th v-for="(header, index) in headers" :key="index">{{ header }} </th >  -->
          <th> Strategy </th>
          <th> Selected Stock </th>
          <th> Date </th>
          <th> Punched At </th>
          <th> Strike Prices </th>
          <!-- <th> Selected Options </th> -->
          <th> Selected Strike </th>
          <th> Selected TF </th>
          <th> Lot </th>
          <th> Reason </th>

        </tr>
      </thead>
      <tbody>
        <tr v-for="(row_item, index) in stopped_records" :key="index">
          <!-- <td v-for="key in Object.keys(record)" :key="key">{{ record[key] }}</td> -->

          <td>{{ row_item.strategy }}</td>
          <td>{{ row_item.selectedStock }}</td>
          <td>{{ row_item.selectedDate }}</td>
          <td>{{ row_item.punchedAt }}</td>
          <td>{{ row_item.choosenStrike }}</td>
          <!-- <td>{{ row_item.selectedOptions }}</td> -->
          <td>{{ row_item.selectedStrike }}</td>
          <td>{{ row_item.selectedTF }}</td>
          <td>{{ row_item.selectedLot }}</td>
          <td>{{ row_item.reason }}</td>

        </tr>
      </tbody>
    </table>
    <p v-else>No records found.</p>
  </div>

</template>

<script>
import axiosInstance from '@/axiosInstance';
import { ref, onMounted } from 'vue';

export default {
  name: 'ApiDataComponent',
  setup() {
    const records = ref([]);
    const headers = ref([]);
    const stopped_records = ref([]);

    // Fetch data from the API
    const fetchData = async () => {
      debugger;
      try {


        const response = await axiosInstance.post('/api/get_running');

        records.value = response.data.message;
        stopped_records.value = response.data.stopped;

        // Extract headers from the first record (if exists)
        if (records.value) {
          headers.value = Object.keys(records.value[0]);
        }

      } catch (error) {
        console.error('Error fetching data:', error);
      }
    }


    // Fetch data when the component is mounted
    onMounted(fetchData);

    const stopPattern = async (row_index, row_thread_key) => {
      // debugger;
      try {
        const response = await axiosInstance.post('/api/simple_stop', { 'thread_key': row_thread_key });

        if (response.data.message) {
          alert(response.data.message);
        }

      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    return {
      records,
      headers,
      stopped_records,
      fetchData,
      stopPattern
    };
  },


};
</script>

<style scoped>
.data-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.data-table th,
.data-table td {
  border: 1px solid #ddd;
  padding: 8px;
}

.data-table th {
  background-color: #f4f4f4;
  text-align: left;
}

.data-table tr:nth-child(even) {
  background-color: #f9f9f9;
}

.my-button {
  background-color: #0edbea;
  color: #fff;
  border: none;
  padding: 8px 12px;
  border-radius: 4px;
  cursor: pointer;
}

.stop-button {
  background-color: #ea0e0e;
  color: #fff;
  border: none;
  padding: 8px 12px;
  border-radius: 4px;
  cursor: pointer;
}
</style>
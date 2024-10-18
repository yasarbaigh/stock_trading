
<template>
  <div id="app">
    <router-view></router-view>
    <ApiDataComponent />
  </div>
</template>

<script>
import ApiDataComponent from './components/stocks/Running_Pattern_Page.vue';

export default {
  name: 'App',
  components: [ApiDataComponent,]
};
</script>

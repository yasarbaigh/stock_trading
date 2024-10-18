const { defineConfig } = require('@vue/cli-service')
// module.exports = defineConfig({
//   transpileDependencies: true
// })

module.exports = {
  devServer: {
    host: '0.0.0.0',
    port: 3002, // Replace 3000 with your desired port number
    hot: true, // Enable Hot Module Replacement (HMR)
    https: false,
    // disableHostCheck: true,
    // allowedHosts: [
    //   '127.0.0.1',
    //   'localhost',
    //   'my_pv_ip',
    //   'chyr.duckdns.org',     
    // ],
    allowedHosts: 'all',
    proxy: {
      '/api': {
        target: process.env.VUE_APP_API_BASE_URL,
        changeOrigin: true,
        secure: false,
        pathRewrite: { '^/api': '' },
        withCredentials: true,
      },
    },
  },
  configureWebpack: {
    // Disable performance hints for faster build during development
    performance: {
      hints: false,
    },
    optimization: {
      splitChunks: false, // Disable chunk splitting for a quicker build in dev mode
    },

  },
  transpileDependencies: [],
  lintOnSave: false,
  chainWebpack: config => {
    config.module
      .rule('js')
      .use('thread-loader')
      .loader('thread-loader')
      .options({ workers: 2 }); // Adjust workers based on your CPU cores
  }

};
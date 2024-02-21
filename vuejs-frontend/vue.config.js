// module.exports = {
//     devServer: {
//       proxy: {
//         '^/users': {
//           target: 'http://localhost:8000/',
//           ws: true,
//           changeOrigin: true
//         },
//       }
//     }
//   }
module.exports = {
    // options...
    devServer: {
          proxy: 'http://localhost:8000/',
          port: 8000
      }
  }
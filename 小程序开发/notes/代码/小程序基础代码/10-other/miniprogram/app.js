App({

  // 全局共享的数据
  globalData: {
    token: ''
  },

  // 全局共享的方法
  setToken (token) {
    // 如果想获取 token，可以使用 this 的方式进行获取
    this.globalData.token = token

    // 在 App() 方法中如果想获取 App() 实例，可以通过 this 的方式进行获取
    // 不能通过 getApp() 方法获取
  }

})
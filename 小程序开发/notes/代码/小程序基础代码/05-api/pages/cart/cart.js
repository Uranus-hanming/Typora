Page({


  navigateTo() {

    // 保留当前页面，跳转到应用中其他页面，不能跳转到 tabBar 页面
    wx.navigateTo({
      url: '/pages/list/list?id=1&name=tom'
      // url: '/pages/cate/cate'
    })

  },

  redirectTo() {

    // 关闭(销毁)当前页面，跳转到应用中其他页面，不能跳转到 tabBar 页面
    wx.redirectTo({
      url: '/pages/list/list?id=1&name=tom'
      // url: '/pages/cate/cate'
    })

  },

  switchTab() {

    // 跳转到 tabBar 页面，不能跳转到 非 tabBar 页面，路径后面不能传递参数
    wx.switchTab({
      // url: '/pages/list/list'
      url: '/pages/cate/cate?id=1&name=tom'
    })

  },

  reLaunch() {

    // 关闭所有的页面，然后跳转到应用中某一个页面
    wx.reLaunch({
      url: '/pages/list/list?id=1&name=tom'
      // url: '/pages/cate/cate?id=1&name=tom'
    })

  }

})
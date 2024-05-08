// list.js
Page({

  navigateBack() {

    // 关闭当前页面，返回上一页或者返回多级页面
    // 默认返回上一页
    wx.navigateBack({
      delta: 1
    })

  },

  onLoad(options) {
    console.log(options)
  }

})

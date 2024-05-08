Page({

  /**
   * 页面的初始数据
   */
  data: {
    
  },

  /**
   * 生命周期函数--监听页面加载--一个页面只会调用一次
   */
  onLoad: function (options) {
    console.log('onLoad 页面创建的时候执行')
  },

  /**
   * 生命周期函数--监听页面初次渲染完成--一个页面只会调用一次
   */
  onReady: function () {
    console.log('onReady 页面初次渲染完成，代表页面已经准备妥当，可以和视图层进行交互')
  },

  /**
   * 生命周期函数--监听页面显示--如果从后台进入前台
   */
  onShow: function () {
    console.log('onShow 页面在前台展示的时候')
  },

  /**
   * 生命周期函数--监听页面隐藏--在当前小程序进入后台时，也会触发执行
   */
  onHide: function () {
    console.log('onHide 页面隐藏')
  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {
    console.log('onUnload 页面卸载、销毁')
  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {
    
  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {
    
  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {
    
  }
})
Page({

  data: {
    num: 1
  },

  handler () {
    this.setData({
      num: this.data.num + 1
    })
  },

  
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    console.log('🥈小程序页面 - profile - onLoad')
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady() {
    console.log('🥈小程序页面 - profile - onReady')
  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow() {
    console.log('🥈小程序页面 - profile - onShow')
  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide() {
    console.log('🥈小程序页面 - profile - onHide')
  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload() {
    console.log('🥈小程序页面 - profile - onUnload')
  }

})

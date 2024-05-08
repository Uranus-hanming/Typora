
Page({

  data: {
    numList: [1, 2, 3],
    isTriggered: false
  },

  refreshHandler () {

    wx.showToast({
      title: '下拉刷新...'
    })
    
    setTimeout(() => {
      this.setData({
        numList: [1, 2, 3],
        isTriggered: false
      })
    }, 2000)

  },


  // scroll-view 上拉加载更多事件的事件处理函数
  getMore () {

    
    wx.showLoading({
      title: '数据加载中...'
    })

    setTimeout(() => {
      // 获取数组的最后一项
      const lastNum = this.data.numList[this.data.numList.length - 1]
      // 定义需要追加的元素
      const newArr = [lastNum + 1, lastNum + 2, lastNum + 3]

      this.setData({
        numList: [...this.data.numList, ...newArr]
      })

      wx.hideLoading()
    }, 1500)


  }

})

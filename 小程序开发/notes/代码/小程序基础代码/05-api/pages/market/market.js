Page({

  data: {
    numList: [1, 2, 3]
  },

  // 监听用户上拉加载
  onReachBottom() {
    // console.log('监听用户上拉加载')
    // 产品需求：
    // 当用户上拉，需要数字进行累加

    // 当用户上拉加载时，需要对数字进行累加，每次累加 3 个数字
    // 目前是 [1, 2, 3]，[1, 2, 3, 4, 5, 6]
    // 怎么进行追加 ？
    // 获取目前数组中最后一项 n，n + 1, n + 2, n + 3

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

  },

  // 监听用户下拉刷新
  onPullDownRefresh () {
    // console.log('监听用户下拉刷新')

    // 产品需求：
    // 当用户上拉加载更多以后，如果用户进行了下拉刷新
    // 需要将数据进行重置
    this.setData({
      numList: [1, 2, 3]
    })

    // 在下拉刷新以后，loading 效果有可能不会回弹回去
    if (this.data.numList.length === 3) {
      wx.stopPullDownRefresh()
    }
  }

})

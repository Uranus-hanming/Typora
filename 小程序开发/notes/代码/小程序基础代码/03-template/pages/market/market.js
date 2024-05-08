
Page({

  data: {
    num: 1,
    isFlag: true
  },


  // 更新 num
  updateNum () {

    this.setData({
      num: this.data.num + 1
    })

  }

})
Page({

  data: {
    num: 1
  },

  handler () {
    this.setData({
      num: this.data.num + 1
    })
  }

})

Page({

  data: {
    num: ''
  },

  getData (event) {
    // 可以通过事件对象.detail 获取子组件传递给父组件的数据
    // console.log(event)
    this.setData({
      num: event.detail
    })
  }

})

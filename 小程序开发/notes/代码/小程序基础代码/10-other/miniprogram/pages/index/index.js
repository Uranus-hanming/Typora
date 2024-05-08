Page({

  // 点击按钮触发的事件处理函数
  handler () {

    wx.navigateTo({
      url: '/pages/list/list',
      events: {
        // key：被打开页面通过 eventChannel 发射的事件
        // value：回调函数
        // 为事件添加一个监听器，获取到被打开页面传递给当前页面的数据
        currentevent: (res) => {
          console.log(res)
        }
      },
      success (res) {
        // console.log(res)
        // 通过 success 回调函数的形参，可以获取 eventChannel 对象
        // eventChannel 对象给提供了 emit 方法，可以发射事件，同时携带参数
        res.eventChannel.emit('myevent', { name: 'tom' })
      }
    })

  }

})
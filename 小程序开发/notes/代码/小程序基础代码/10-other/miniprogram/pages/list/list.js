Page({

  onLoad () {

    // 通过 this.getOpenerEventChannel() 可以获取 EventChannel 对象
    const EventChannel = this.getOpenerEventChannel()

    // 通过 EventChannel 提供的 on 方法监听页面发射的自定义事件
    EventChannel.on('myevent', (res) => {
      console.log(res)
    })

    // 通过 EventChannel 提供的 emit 方法也可以向上一级页面传递数据
    // 需要使用 emit 定义自定义事件，携带需要传递的数据
    EventChannel.emit('currentevent', { age: 10 })

  }

})
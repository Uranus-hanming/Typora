import PubSub from 'pubsub-js'

Component({

  // 组件的初始数据
  data: {
    name: ''
  },

  // 组件的方法列表
  methods: {

  },

  lifetimes: {
    attached () {

      // subscribe 订阅、监听自定义的事件
      // 1. 需要订阅、监听的自定义事件名称
      // 2. 回调函数，回调函数有两个参数
      //   2.1  msg：自定义事件的名称
      //   2.2  data：传递过来的数据
      PubSub.subscribe('myevent', (msg, data) => {
        console.log(msg, data)

        this.setData({
          name: data.name
        })
      })

    }
  }
})

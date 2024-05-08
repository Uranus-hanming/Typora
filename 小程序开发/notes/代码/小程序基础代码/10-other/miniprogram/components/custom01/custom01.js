import PubSub from 'pubsub-js'

Component({

  // 组件的初始数据
  data: {
    name: 'tom'
  },

  // 组件的方法列表
  methods: {
    sendData () {

      // publish 发布、发射自定义事件
      // 1. 自定义事件的名称
      // 2. 需要传递的数据
      PubSub.publish('myevent', { name: this.data.name, age: 10 })

    }
  }
})

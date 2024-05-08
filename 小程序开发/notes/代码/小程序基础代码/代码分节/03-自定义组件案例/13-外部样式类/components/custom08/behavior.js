

const behavior = Behavior({
  /**
   * 组件的属性列表
   */
  properties: {
    label: {
      type: String,
      value: '我已同意该协议'
    }
  },

  /**
   * 组件的初始数据
   */
  data: {
    name: 'Tom',
    obj: {
      name: 'Tyke'
    }
  },

  /**
   * 组件的方法列表
   */
  methods: {
    updateName () {
      this.setData({
        name: 'Jerry'
      })

      console.log('我是 behavior 内部的方法 ！！！！')
    }
  },

  lifetimes: {
    attached () {
      console.log('我是 behavior 的生命周期函数 ~~~~~~~~~~~')
    }
  }
})

export default behavior

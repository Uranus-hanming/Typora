Component({

  // 为什么需要使用 Component 方法进行构造页面
  // Component 方法功能比 Page 方法强大很多
  // 如果使用 Component 方法构造页面，可以实现更加复杂的页面逻辑开发

  // 小程序页面也可以使用 Component 方法进行构造
  // 注意事项：
  // 1. 要求 .json 文件中必须包含 usingComponents 字段
  // 2. 里面的配置项需要和 Component 中的配置项保持一致
  // 3. 页面中 Page 方法有一些钩子函数、事件监听方法，这些钩子函数、事件监听方法必须方法 methods 对象中
  // 4. 组件的属性 properties 也可以接受页面的参数，在 onLoad 钩子函数中可以通过 this.data 进行获取

  properties: {
    id: String,
    title: String
  },

  data: {
    name: 'tom'
  },

  // onLoad () {
  //   console.log('页面加载 - 1')
  // },

  methods: {

    // 更新 name
    updateName() {
      this.setData({
        name: 'jerry'
      })
    },

    onLoad (options) {
      // console.log('页面加载 - 2')
      // console.log(options)
      console.log(this.data.id)
      console.log(this.data.title)
      console.log(this.properties.id)
    },

  }

})
// index.js
Page({

  parentHandler () {
    console.log('父组件绑定的事件')
  },

  btnHandler () {
    console.log('子组件触发的事件')
  },

  // 事件处理函数需要写到 Page() 方法中才可以
  handler (event) {
    // console.log('事件触发了~~~~')
    console.log(event)
  },

  getInputVal (event) {
    console.log(event.detail.value)
  }

})

// cart.js
Page({

  // 按钮绑定的事件处理函数
  btnHandler (event) {
    console.log(event.mark.id)
    console.log(event.mark.name)
  },

  // view 绑定的事件处理函数
  parentHandler (event) {
    // 先点击蓝色区域 (不点击按钮)
    // 通过事件对象获取的是 view 身上绑定的数据

    // 先点击按钮 (不点击蓝色区域)
    // 通过事件对象获取到的是 触发事件的节点 已经 父节点身上所有的 mark 数据
    console.log(event)
  }

})

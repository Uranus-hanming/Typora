// cate.js
Page({

  // 按钮触发的事件处理函数
  btnHandler (event) {
    // currentTarget 事件绑定者，也就是指：哪个组件绑定了当前事件处理函数
    // target 事件触发者，也就是指：哪个组件触发了当前事件处理函数
    // currentTarget 和 target 都是指按钮，因为是按钮绑定的事件处理函数，同时点击按钮触发事件处理函数
    // 这时候通过谁来获取数据都可以
    console.log(event.currentTarget.dataset.id)
    console.log(event.target.dataset.name)
  },


  // view 绑定的事件处理函数
  parentHandler (event) {
    // 点击蓝色区域(不点击按钮)
    // currentTarget 事件绑定者：view
    // target 事件触发者：view
    // currentTarget 和 target 都是指 view，如果想获取 view 身上的数据，使用谁都可以

    // 点击按钮(不点击蓝色区域)
    // currentTarget 事件绑定者：view
    // target 事件触发者：按钮
    // 如果想获取 view 身上的数据，就必须使用 currentTarget 才可以
    // 如果想获取的是事件触发者本身的数据，就需要使用 target
    console.log(event)

    // 在传递参数的时候，如果自定义属性是多个单词，单词与单词直接使用中划线 - 进行连接
    // 在事件对象中会被转换为小托峰写法
    console.log(event.currentTarget.dataset.parentId)

    // 在传递参数的时候，如果自定义属性是多个单词，单词如果使用的是小托峰写法
    // 在事件对象中会被转为全部小写的
    console.log(event.currentTarget.dataset.parentname)
  }

})

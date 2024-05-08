// components/custom04/custom04.js
Component({

  /**
   * 组件的属性列表
   */
  properties: {
    label: {
      type: String,
      value: '测试'
    }
  },

  /**
   * 组件的初始数据
   */
  data: {
    num: 10,
    count: 100,
    obj: { name: 'Tom', age: 10 },
    arr: [1, 2, 3]
  },

  // 用来监听数据以及属性是否发生了变化
  observers: {

    // key：需要监听的数据
    // value：就是一个回调函数，形参：最新的数据
    num: function (newNum) {
      // 对 data 中的数据进行监听，如果数据没有发生改变，监听器不会执行
      console.log(newNum)
    },

    // count: function (newCount) {
    //   console.log(newCount)
    // }

    // 同时监听多个数据
    // 'num, count': function (newNum, newCount) {
    //   console.log(newNum, newCount)
    // }

    // 支持监听属性以及内部数据的变化
    // 'obj.name': function (newName) {
    //   console.log(newName)
    // },

    // 'arr[1]': function (newItem) {
    //   console.log(newItem)
    // }

    // 使用通配符
    // 'obj.**': function (newObj) {
    //   console.log(newObj)
    // }

    label: function (newLabel) {
      // 只要组件使用者传递了数据，这时候在监听器中就能获取传递的数据
      // 也就是说，监听器立即就执行了
      console.log(newLabel)
    }

  },

  /**
   * 组件的方法列表
   */
  methods: {

    // 更新数据
    updateData () {

      this.setData({
        num: this.data.num + 1,
        // count: this.data.count - 1
        // 'obj.name': 'jerry',
        // 'arr[1]': 666
        label: '最新的标题'
      })

    }

  }
})
Page({

  data: {
    isChecked: true
  },

  getData (event) {
    console.log(event.detail)

    if (event.detail) {
      console.log('提交')
    } else {
      console.log('请同意协议！')
    }
  },

  // 获取子组件的实例对象
  getChild () {

    // this.selectComponent 方法获取子组件实例对象
    // 获取到实例对象以后，就能获取子组件所有的数据、也能调用子组件的方法
    const res = this.selectComponent('#child')
    console.log(res.data.isChecked)

  }

})
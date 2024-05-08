// components/custom06/custom06.js
Component({

  data: {
    name: 'tom'
  },

  // 组件生命周期声明对象
  lifetimes: {

    // created：组件实例被创建好以后执行
    created () {
      console.log('组件 created')

      // 所以在 created 钩子函数中不能调用 setData
      // 可以给组件添加一些自定义的属性，可以通过 this 的方式进行添加
      this.test = '测试'
      // this.setData({
      //   name: 'jerry'
      // })
    },

    // 组件被初始化完毕，模板解析完成，已经把组件挂载到页面上
    attached () {
      console.log('组件 attached')
      console.log(this.test)

      // 一般页面中的交互会在 attached 钩子函数中进行执行
      this.setData({
        name: 'jerry'
      })
    },

    // 组件被销毁时
    detached () {
      console.log('组件 detached')
    }

  }

})
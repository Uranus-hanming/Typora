Component({

  /**
   * 组件的属性列表
   */
  properties: {

  },

  /**
   * 组件的初始数据：用来定义当前组件内部所需要使用的数据
   */
  data: {
    isChecked: false
  },

  /**
   * 组件的方法列表：在组件中，所有的事件处理程序都需要写到 methods 方法中
   */
  methods: {
    
    // 更新复选框的状态
    updateChecked () {

      this.setData({
        isChecked: !this.data.isChecked
      })

      console.log(this.data.isChecked)
    }

  }
  
})
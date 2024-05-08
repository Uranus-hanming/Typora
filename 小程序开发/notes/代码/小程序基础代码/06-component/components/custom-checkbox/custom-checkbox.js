Component({

  options: {
    styleIsolation: 'shared'
  },

  // 如果 styleIsolation 属性值是 shared
  // 这时候呢 externalClasses 选项会失效
  externalClasses: ['xxxx'],

  /**
   * 组件的属性列表：组件的对外属性，主要用来接收组件使用者传递给组件内部的属性以及数据
   */
  properties: {
    // 如果需要接收传递的属性，有两种方式：全写、简写
    // label: String

    label: {
      // type 组件使用者传递的数据类型
      // 数据类型：String、Number、Boolean、Object、Array
      // 也可以设置为 null，表示不限制类型
      type: String,
      value: ''
    },

    position: {
      type: String,
      value: 'right'
    },

    // 复选框组件公共组件
    // 需要再多个页面、在多个项目中进行使用
    // 在使用的时候，有的地方希望默认是选中的效果，有的地方希望默认是没有被选中的效果
    // 怎么处理 ？
    // 首先让复选框默认还是没有被选中的效果
    // 如果希望复选框默认被选中，这时候传递属性(checked=true)到复选框组件
    checked: {
      type: Boolean,
      value: false
    }
  },

  /**
   * 组件的初始数据：用来定义当前组件内部所需要使用的数据
   */
  data: {
    isChecked: false
  },

  observers: {
    // 如果需要将 properties 中的数据赋值给 data
    // 可以使用 observers 进行处理
    checked: function (newChecked) {
      // console.log(newChecked)
      this.setData({
        isChecked: newChecked
      })
    }
  },

  /**
   * 组件的方法列表：在组件中，所有的事件处理程序都需要写到 methods 方法中
   */
  methods: {
    
    // 更新复选框的状态
    updateChecked () {

      this.setData({
        isChecked: !this.data.isChecked,
        // label: '在组件内部也可以修改 properties 中的数据'
      })

      // 在 JS 中可以访问和获取 properties 中的数据
      // 但是一般情况下，不建议修改，因为会造成数据流的混乱
      // console.log(this.properties.label)
      // console.log(this.data.isChecked)

      // 目前复选框组件的状态是存储在复选框组件内部的、存储在自定义组件内部的
      // 但是，在以后实际开发中，组件使用者、父组件有时候也需要获取到复选框内部的状态
      // 怎么办 ？
      // 这时候，自定义组件内部就需要发射一个自定义事件，
      // 如果组件使用者、父组件需要使用数据，绑定自定义事件进行获取即可
      this.triggerEvent('changechecked', this.data.isChecked)
    }

  }
  
})
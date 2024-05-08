// components/custom03/custom03.js
Component({

  options: {

    // styleIsolation：配置组件样式隔离

    // isolated：开启样式隔离，默认值
    // 在默认情况下，自定义组件和组件使用者如果存在相同的类名，类名不会相互影响

    // apply-shared：表示组件使用者、页面的 wxss 样式能够影响到自定义组件
    // 但是自定义组件的样式不会影响组件使用者、页面的 wxss 样式
    // styleIsolation: "apply-shared"

    // shared：表示组件使用者、页面的 wxss 样式能够影响到自定义组件
    // 自定义组件的样式会影响组件使用者、页面的 wxss 样式
    // 和其他使用了 apply-share 以及 share 属性的自定义组件
    styleIsolation: 'shared'

  },

  /**
   * 组件的属性列表
   */
  properties: {

  },

  /**
   * 组件的初始数据
   */
  data: {

  },

  /**
   * 组件的方法列表
   */
  methods: {

  }
})
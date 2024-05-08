// 执行 extendApi.js 文件，将方法挂载到 wx 全局对象身上
import './utils/extendApi'

App({
  // globalData 是指全局共享的数据
  // 点击收货地址时，需要将点击的收货地址赋值给 address
  // 在结算支付、订单结算页面，需要判断 address 是否存在数据
  // 如果存在数据，就展示 address 数据，如果没有数据，就从接口获取数据进行渲染
  globalData: {
    address: {}
  },

  onShow() {
    // 获取当前小程序的账号信息
    // const accountInfo = wx.getAccountInfoSync()
    // 通过小程序的账号信息，就能获取小程序版本
    // console.log(accountInfo.miniProgram.envVersion)
  }
})

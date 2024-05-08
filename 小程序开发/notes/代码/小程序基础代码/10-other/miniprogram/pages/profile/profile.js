// getApp() 方法用来获取全局唯一的 App() 实例
const appInstance = getApp()

Page({

  login () {

    // 不要通过 app 实例调用钩子函数
    console.log(appInstance)

    appInstance.setToken('fghioiuytfghjkoiuytghjoiug')

  }

})
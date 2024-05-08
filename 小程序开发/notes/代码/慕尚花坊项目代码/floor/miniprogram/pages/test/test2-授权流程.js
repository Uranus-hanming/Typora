Page({
  // 拒绝授权后的处理方案-演示问题
  async onLocation1() {
    try {
      // 获取用户地理位置信息
      // 在用户拒绝授权以后，如果再次调用 getLocation，不会在弹出授权弹窗
      const res = await wx.getLocation()
      console.log(res)
    } catch (error) {
      wx.toast({ title: '您拒绝授权获取地理位置' })
    }
  },

  // 拒绝授权后的处理方案-获取授权状态
  async onLocation2() {
    // 调用 wx.getSetting 获取用户所有的授权信息，查询到用户是否授权了位置信息
    // authSetting 只包含了小程序向用户请求的所有的权限，同时包含了授权的结果(true、false)
    const { authSetting } = await wx.getSetting()

    // scope.userLocation 用户是否授权获取了地理位置信息
    // 如果小程序没有向用户发起过授权请求，authSetting 中没有 scope.userLocation 属性
    // 如果用户点击了允许授权，返回值就是 true
    // 如果用户点击了拒绝授权，返回值就是 false
    console.log(authSetting['scope.userLocation'])
  },

  // 拒绝授权后的处理方案-整体的逻辑
  async onLocation() {
    // authSetting 获取小程序已经向用户申请的权限，并且会返回授权的结果
    const { authSetting } = await wx.getSetting()
    // scope.userLocation 用户是否授权小程序获取位置信息
    console.log(authSetting['scope.userLocation'])

    // 判断用户是否拒绝了授权
    if (authSetting['scope.userLocation'] === false) {
      // 用户之前拒绝授权获取位置信息，用户再次发起了授权
      // 这时候需要使用一个弹框询问用户是否进行授权
      const modalRes = await wx.modal({
        title: '授权提示',
        content: '需要获取地理位置信息，请确认授权'
      })

      // 如果用户点击了取消，说明用户拒绝了授权，需要给用户进行提示
      if (!modalRes) return wx.toast({ title: '您拒绝了授权' })

      // 如果用户点击了确定，说明用户同意授权，需要打开微信客户端小程序授权页面
      const { authSetting } = await wx.openSetting()

      // 如果用户没有更新授权信息，需要给用户提示授权失败
      if (!authSetting['scope.userLocation'])
        return wx.toast({ title: '授权失败' })

      //如果用户更新了授权信息，说明用户同意授权获取位置信息
      try {
        const locationRes = await wx.getLocation()
        console.log(locationRes)
      } catch (error) {
        wx.toast({ title: '您拒绝授权获取位置信息' })
      }
    } else {
      try {
        const locationRes = await wx.getLocation()
        console.log(locationRes)
      } catch (error) {
        wx.toast({ title: '您拒绝授权获取位置信息' })
      }
    }
  }
})

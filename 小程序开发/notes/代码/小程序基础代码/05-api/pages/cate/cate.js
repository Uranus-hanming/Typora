Page({


  // 将数据存储到本地
  setStorage () {

    // 第一个参数：本地存储中指定的 key
    // 第二个参数：需要存储的数据
    // wx.setStorageSync('num', 1)

    // 在小程序中
    // 如果存储的是对象类型数据，不需要使用 JSON.stringify 和 JSON.parse 进行转换
    // 直接进行存储和获取即可
    // wx.setStorageSync('obj', { name: 'tom', age: 10 })

    // ------------------- 异步 API -------------------
    wx.setStorage({
      key: 'num',
      data: 1
    })

    wx.setStorage({
      key: 'obj',
      data: { name: 'jerry', age: 18 }
    })

  },

  // 获取本地存储的数据
  async getStorage () {

    // 从本地存储的数据中获取指定 key 的数据、内容
    // const num = wx.getStorageSync('num')
    // const obj = wx.getStorageSync('obj')

    // console.log(num)
    // console.log(obj)

    // ------------------- 异步 API -------------------

    const { data } = await wx.getStorage({
      key: 'obj'
    })

    console.log(data)

  },

  // 删除本地存储的数据
  removeStorage () {

    // 从本地移除指定 key 的数据、内容
    // wx.removeStorageSync('num')

    // ------------------- 异步 API -------------------

    wx.removeStorage({
      key: 'num'
    })

  },

  // 清空本地存储的全部数据
  clearStorage () {
    // wx.clearStorageSync()

    wx.clearStorage()
  },

})

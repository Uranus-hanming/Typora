import instance from '@/utils/http'

// 导入接口 API 函数
import { reqSwiperData } from '@/api/index'

Page({
  data: {
    avatarUrl: '@/assets/Jerry.png'
  },

  // 获取微信头像
  async chooseavatar(event) {
    // console.log(event)

    // 目前获取的微信头像是临时路径
    // 临时路径是有失效时间的，在实际开发中，需要将临时路径上传到公司的服务器
    const { avatarUrl } = event.detail

    const { data: avatar } = await instance.upload('/fileUpload', avatarUrl, 'file')

    this.setData({
      avatarUrl: avatar
    })

    // wx.uploadFile({
    //   // 开发者服务器地址、接口地址
    //   url: 'https://gmall-prod.atguigu.cn/mall-api/fileUpload',
    //   // 要上传的文件路径
    //   filePath: avatarUrl,
    //   // 文件对应的 key，服务器需要根据 key 来获取文件的二进制信息
    //   name: 'file',

    //   success: (res) => {
    //     // 服务器返回的数据是 JSON 字符串，在使用的时候，需要进行转换 JSON.parse 进行转换
    //     res.data = JSON.parse(res.data)

    //     this.setData({
    //       avatarUrl: res.data.data
    //     })
    //   }
    // })

    // this.setData({
    //   avatarUrl
    // })
  },

  async handler() {
    const res = await reqSwiperData()

    console.log(res)

    // 第一种调用方式，.then 的方式进行调用
    // instance
    //   .request({
    //     url: 'https://gmall-prod.atguigu.cn/mall-api/index/findBanner',
    //     method: 'GET'
    //   })
    //   .then((res) => {
    //     console.log(res)
    //   })

    // 第二种调用方式，通过 await 和 async 的方式进行调用
    // const res = await instance.request({
    //   url: '/index/findBanner',
    //   method: 'GET'
    // })

    // /cart/getCartList
    // const res = await instance.get('/index/findBanner', null, {
    //   isLoading: true
    // })
    // console.log(res)

    // const res = await instance.get('/index/findBanner')
    // console.log(res)

    // instance.get('/index/findBanner').then(() => {
    //   instance.get('/index/findBanner').then(() => {})
    // })
  },

  handler1() {
    wx.request({
      url: 'https://gmall-prod.atguigu.cn/mall-api/index/findBanner',
      method: 'GET',
      // timeout: 100,
      success: (res) => {
        // 在使用 wx.request 发送请求时
        // 只要成功接收到服务器返回的结果
        // 无论 statusCode、状态码是多少，都会执行 success
        // 开发者就需要根据业务逻辑，自己来进行相关的判断处理
        console.log('虽然接口错了，但是我依然会走 success')
        console.log(res)
      },
      fail: (err) => {
        // 一般在网络出现异常时(网络超时)，就会执行 fail
        console.log('网络超时了，这时候网络出现了异常，就会执行 fail')
        console.log(err)
      }
    })
  },

  // 测试并发请求
  async allHandler() {
    // 演示通过 async 和 await 方式同时发起多个请求
    // async 和 await 能够控制异步任务以同步的流程来执行

    // async 和 await 方式发起多个请求
    // 当第一个请求结束以后，才能够发起第二个请求
    // 在前一个请求结束以后，才能够发起下一个请求
    // 会造成请求的阻塞，从而影响页面的渲染速度
    // await instance.get('/index/findBanner')
    // await instance.get('/index/findCategory1')
    // await instance.get('/index/findBanner')
    // await instance.get('/index/findCategory1')

    // 演示通过 Promise.all 同时发起多个请求
    // Promise.all 能够将多个请求同时进行发送
    // Promise.all 能够将多个异步请求同时进行发送，也就是并行发送
    // 并不会造成请求的阻塞，从而不会影响页面的渲染速度
    // await Promise.all([instance.get('/index/findBanner'), instance.get('/index/findCategory1'), instance.get('/index/findBanner'), instance.get('/index/findCategory1')])

    const res = await instance.all(
      instance.get('/index/findBanner'),
      instance.get('/index/findCategory1'),
      instance.get('/index/findBanner'),
      instance.get('/index/findCategory1'),
      instance.get('/index/findBanner'),
      instance.get('/index/findCategory1'),
      instance.get('/index/findBanner'),
      instance.get('/index/findBanner'),
      instance.get('/index/findCategory1'),
      instance.get('/index/findBanner'),
      instance.get('/index/findCategory1'),
      instance.get('/index/findBanner'),
      instance.get('/index/findCategory1'),
      instance.get('/index/findBanner')
    )

    console.log(res)
  }
})

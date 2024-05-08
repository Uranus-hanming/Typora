Page({

  data: {
    avatarUrl: '../../assets/Jerry.png'
  },


  // 获取微信头像
  chooseavatar (event) {
    // console.log(event)

    // 目前获取的微信头像是临时路径
    // 临时路径是有失效时间的，在实际开发中，需要将临时路径上传到公司的服务器
    const { avatarUrl } = event.detail

    this.setData({
      avatarUrl
    })

  },

  // 获取微信昵称
  onSubmit (event) {
    // console.log(event.detail.value)
    const { nickname } = event.detail.value
    console.log(nickname)
  }

})
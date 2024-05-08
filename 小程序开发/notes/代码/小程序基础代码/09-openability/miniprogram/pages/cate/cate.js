Page({

  // 监听页面按钮的转发 以及 右上角的转发按钮
  onShareAppMessage (obj) {
    // console.log(obj)

    return {
      title: '这是一个非常神奇的页面~~~',
      path: '/pages/cate/cate',
      imageUrl: '../../assets/Jerry.png'
    }

  },

  // 监听右上角 分享到朋友圈 按钮
  onShareTimeline () {

    return {
      title: '帮我砍一刀~~~',
      query: 'id=1',
      imageUrl: '../../assets/Jerry.png'
    }

  }

})

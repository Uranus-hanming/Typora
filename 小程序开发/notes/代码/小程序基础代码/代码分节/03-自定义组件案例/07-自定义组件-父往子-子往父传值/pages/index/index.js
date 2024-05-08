Page({

  data: {
    isChecked: true
  },

  getData (event) {
    console.log(event.detail)

    if (event.detail) {
      console.log('提交')
    } else {
      console.log('请同意协议！')
    }
  }

})
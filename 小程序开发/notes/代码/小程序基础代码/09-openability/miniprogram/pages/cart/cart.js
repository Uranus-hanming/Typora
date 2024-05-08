Page({

  // 手机号快速验证
  getphonenumber (event) {
    // 通过事件对象，可以看到，在 event.detail 中可以获取到 code
    // code 动态令牌，可以使用 code 换取用户的手机号
    // 需要将 code 发送给后端，后端在接收到 code 以后
    // 也需要调用 API，换取用户的真正手机号
    // 在换取成功以后 ，会将手机号返回给前端
    console.log(event)
  },

  // 手机号实时验证
  getrealtimephonenumber (event) {
    console.log(event)
  },

})
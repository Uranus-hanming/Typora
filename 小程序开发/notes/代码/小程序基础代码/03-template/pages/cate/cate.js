// cate.js
Page({

  data: {
    num: 1,
    userInfo: {
      name: 'tom',
      age: 10,
      test: 111
    },
    list: [1, 2, 3]
    // list: [ { id: 1, name: 'tom' } ]
  },

  // 更新 num
  updateNum () {

    // 获取数据
    // console.log(this.data.num)

    // 通过赋值的方式直接修改数据
    // 能够修改数据，但是不能改变页面上的数据
    // this.data.num += 1

    // console.log(this.data.num)

    // this.setData 两个作用
    // 1. 更新数据
    // 2. 驱动视图（页面）更新
    this.setData({
      // key：是需要更新的数据
      // value：是最新的值
      num: this.data.num + 1
    })

  },

  // 更新 userInfo
  updateUserInfo () {

    // 新增单个 / 多个属性
    // this.setData({
    //   // 如果给对象新增属性，可以将 key 写成数据路径的方式 a.b.c
    //   'userInfo.name': 'tom',
    //   'userInfo.age': 10
    // })

    // 修改单个 / 多个属性
    // this.setData({
    //   // 如果需要修改对象属性，也可以将 key 写成数据路径的方式 a.b.c
    //   'userInfo.name': 'jerry',
    //   'userInfo.age': 18
    // })

    // 目前进行新增和修改都是使用数据路径，如果新增和修改的数据量比较小，还可以
    // 如果修改的数据很多，每次都写数据路径，就太麻烦了
    // 可以使用 ES6 提供的展开运算符 和 Object.assign()

    // ES6 提供的展开运算符
    // 通过展开运算符能够将对象中的属性复制给另一个对象
    // 后面的属性会覆盖前面的属性
    // const userInfo = {
    //   ...this.data.userInfo,
    //   name: 'jerry',
    //   age: 18
    // }

    // this.setData({
    //   userInfo
    // })

    // Object.assign() 将多个对象合并为一个对象
    // const userInfo = Object.assign(this.data.userInfo, { name: 'jerry' }, { age: 18 })
    // this.setData({
    //   userInfo
    // })

    // 删除单个属性
    // delete this.data.userInfo.age
    // // console.log(this.data.userInfo)
    // this.setData({
    //   userInfo: this.data.userInfo
    // })

    // 删除多个属性 rest 剩余参数
    const { age, test, ...rest } = this.data.userInfo

    this.setData({
      userInfo: rest
    })

  },

  // 更新 list
  updateList () {

    // 新增数组元素
    // 如果直接使用 push 方法，可以直接更新 data ，但是不能更新 页面中的数据
    // this.data.list.push(4)
    // this.data.list.push(4)
    // this.setData({
    //   list: this.data.list
    // })

    // const newList = this.data.list.concat(4)
    // this.setData({
    //   list: newList
    // })

    // const newList = [ ...this.data.list, 4 ]
    // this.setData({
    //   list: newList
    // })

    // 修改数组元素
    // this.setData({
    //   // 'list[1]': 6
    //   'list[0].name': 'jerry'
    // })

    // 删除数组元素
    // this.data.list.splice(1, 1)
    // this.setData({
    //   list: this.data.list
    // })

    const newList = this.data.list.filter(item => item !== 2)
    this.setData({
      list: newList
    })

  }
})

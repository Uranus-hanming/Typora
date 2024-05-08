// 从 async-validator 中引入构造函数
import Schema from 'async-validator'

Page({
  data: {
    name: ''
  },

  // 对数据进行验证
  onValidator() {
    // 定义验证规则
    const rules = {
      // key 验证规则的名字，名字需要和验证的数据保持一致
      name: [
        // required 是否是必填项
        // message 如果验证失败，提示错误内容
        { required: true, message: 'name 不能为空' },

        // type 验证数据的类型
        { type: 'string', message: 'name 不是字符串' },

        // min 最少位数，max 最大位数
        { min: 2, max: 3, message: '名字最少 2 个字，最多是 3 个字' }

        // pattern 使用正则对数据进行验证
        // { pattern: '', message: '' }

        // validator 自定义验证规则
        // { validator: () => {} }
      ]
    }

    // 需要对构造函数进行实例化，同时传入验证规则
    const validator = new Schema(rules)

    // 需要调用 validate 实例方法，对数据进行验证
    // 第一个参数：需要验证的数据，要求数据是一个对象
    //  validate 方法只会验证和验证规则同名的字段
    // 第二个参数：是一个回调函数
    validator.validate(this.data, (errors, fields) => {
      // 如果验证成功，errors 是一个 null
      // 如果验证失败，errors 是一个数组，数组每一项是错误信息

      // fields 是需要验证的属性，属性值是一个数组，数组中也包含着错误信息

      if (errors) {
        console.log('验证失败')

        console.log(errors)

        console.log(fields)
      } else {
        console.log('验证成功')
      }
    })
  }
})

// 导入封装的 接口 API 函数
import { reqCategoryData } from '@/api/category'

Page({
  // 初始化数据
  data: {
    categoryList: [], // 商品分类列表数据
    activeIndex: 0 // 被激活那一项的索引，默认是 0
  },

  // 实现一级分类的切换效果
  updateActive(event) {
    // console.log(event.currentTarget.dataset)
    const { index } = event.currentTarget.dataset

    this.setData({
      activeIndex: index
    })
  },

  // 获取商品分类的数据
  async getCategoryData() {
    const res = await reqCategoryData()

    if (res.code === 200) {
      this.setData({
        categoryList: res.data
      })
    }
  },

  // 监听页面的加载
  onLoad() {
    // 调用获取商品分类的数据的方法
    this.getCategoryData()
  }
})
